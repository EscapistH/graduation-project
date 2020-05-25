<template>
  <el-main v-loading="is_loading">
    <!-- 行 -->
    <el-row :gutter="12" v-for="(each_row, index) in Math.ceil(demands.length/4)" :key="index">
      <!-- 列 -->
      <div v-if="demands.length === 0" style="text-align:center;">没有更多了</div>
      <el-col
        v-else
        v-for="(demand, id) in demands.slice((each_row-1)*4,each_row*4)"
        :key="id"
        :span="6"
      >
        <!-- 卡片 -->
        <div class="card-box">
          <!-- 鼠标覆盖时出现卡片阴影 -->
          <el-card shadow="hover">
            <!-- 卡片标题 -->
            <div class="card-title">
              <span class="hospital-name">{{demand.publisher}}</span>
              <!-- tag 验证 -->
              <el-tag type="success" size="mini" effect="plain" class="review-tag">已验证</el-tag>
              <div class="card-address">{{address_split(demand.address)}}</div>
            </div>
            <!-- 卡片主体 -->
            <div class="card-content">
              <div v-for="(supply, index) in demand.supplies" :key="index" class="supply-item">
                <div class="supply-name">{{supply.name}}</div>
                <div class="supply-number">{{supply.number}}</div>
              </div>
            </div>
            <!-- 卡片底部 -->
            <div class="card-bottom">
              <div
                class="other-supply-num"
                :hidden="demand.supplies.length > 3? false:true"
              >+{{demand.supplies.length-3}} 项其他物资</div>
              <div>
                <div class="demand-info-btn">
                  <el-button type="text" @click="open_demand_info(id)">查看详情</el-button>
                </div>
                <div class="donate-btn">
                  <el-button @click="open_donation_dialog(id)">捐赠</el-button>
                </div>
              </div>
            </div>
            <div class="demand-operate">
              <el-button-group>
                <!-- 点击按钮打开dialog -->
                <el-button type="primary" @click="modify_demand(id)">修改信息</el-button>
                <!-- 修改信息的dialog -->
                <el-dialog
                  title="修改需求信息"
                  :visible.sync="modify_dialog_visible"
                  width="30%"
                  :before-close="handle_close"
                  v-loading="is_modifying"
                >
                  <el-form :model="demand_by_id" label-width="8rem" label-position="left">
                    <el-form-item label="所属医院或单位">
                      <el-input v-model="demand_by_id.title"></el-input>
                    </el-form-item>
                    <el-form-item
                      v-for="(d, name) in demand_by_id.content"
                      :key="name"
                      :label="d.name"
                    >
                      <el-input
                        v-model="d.num"
                        :type="d.name === '其他'?'textarea':'text'"
                        rows="5"
                        class="demand-num"
                      ></el-input>
                    </el-form-item>
                  </el-form>
                  <div slot="footer" class="dialog-footer">
                    <el-button type="success" @click="do_modify">提交修改</el-button>
                  </div>
                </el-dialog>
                <el-button
                  type="warning"
                  @click="do_cancel(id)"
                  :loading="is_canceling"
                  :disabled="is_canceling"
                >撤销发布</el-button>
              </el-button-group>
            </div>
          </el-card>
        </div>
      </el-col>
    </el-row>
    <div class="load-more-btn">
      <el-button
        type="text"
        :loading="is_loading_more"
        :disabled="is_loading_more"
        @click="load_more"
      >加载更多</el-button>
    </div>
  </el-main>
</template>

<script>
export default {
  data() {
    return {
      demands: [],
      demand_by_id: {},
      params: { page: 0, num: 12 },
      modify_dialog_visible: false,
      is_loading_more: false,
      is_modifying: false,
      is_canceling: false
    };
  },

  created() {
    this.get_some_demands();
  },

  methods: {
    handle_close(done) {
      this.$confirm("还未提交修改,确认关闭吗?")
        .then(() => {
          this.demand = null;
          done();
          this.modify_dialog_visible = false;
        })
        .catch(() => {});
    },
    get_some_demands() {
      this.is_loading = true;
      this.$http.get("/my_pub_demands", { params: this.params }).then(
        res => {
          // console.log(res);
          if (res.data.code === 200) {
            this.is_loading = false;
            this.demands = res.data.data;
            // console.log(this.demands);
          }
          if (res.data.code === 401) {
            this.is_loading = false;
            this.$message.warning("登录已过期，请重新登录");
            this.$router.push("/login");
          }
        },
        // 获取数据超时的超时信息
        () => {
          this.is_loading = false;
          this.$message.error("获取数据失败，请重试");
        }
      );
    },
    // 加载更多
    load_more() {
      this.is_loading_more = true;
      this.params.page = Math.ceil(this.demands.length / 12);
      this.$http.get("/my_pub_demands", { params: this.params }).then(
        res => {
          // console.log(res);
          if (res.data.code === 200) {
            this.is_loading_more = false;
            if (res.data.data.length === 0) {
              this.is_loading_more = false;
              return this.$message.warning("没有更多了");
            }
            for (let i = 0; i < res.data.data.length; i++) {
              const new_demand = res.data.data[i];
              this.demands.push(new_demand);
            }
          }
        },
        () => {
          this.$message.warning("获取数据失败，请重试");
        }
      );
    },
    // 根据demand id打开对应的modify dialog并传入数据
    modify_demand(d_id) {
      this.modify_dialog_visible = true;
      this.demand_by_id = this.demands[d_id];
    },
    // 点击提交按钮执行更新
    do_modify() {
      // console.log(this.demand_by_id)
      this.is_modifying = true;
      this.$http.post("/modify_demand", this.demand_by_id).then(
        res => {
          // console.log(res);
          if (res.data.code === 200) {
            this.$message.success("更新成功");
            this.modify_dialog_visible = false;
            this.is_modifying = false;
          }
          if (res.data.code === 401) {
            this.is_modifying = false;
            this.$message.warning("登录已过期，请重新登录");
            this.$router.push("/login");
          }
        },
        () => {
          this.is_modifying = false;
          this.$message.error("请求失败，请重试");
        }
      );
    },
    do_cancel(d_id) {
      // console.log(this.demands[d_id].id);
      // console.log(this.demands)
      this.is_canceling = true;
      this.$confirm("确认撤销吗?撤销后不可恢复")
        .then(() => {
          this.$http
            .post("/cancel_demand", { id: this.demands[d_id].id })
            .then(res => {
              // console.log(res);
              if (res.data.code === 200) {
                this.is_canceling = false;
                this.$message.success("撤销发布成功");
                this.$router.go(0);
              }
              if (res.data.code === 401) {
                this.is_canceling = false;
                this.$message.warning("登录已过期，请重新登录");
                this.$router.push("/login");
              }
            });
        })
        .catch(() => {
          this.is_canceling = false;
        });
    }
  }
};
</script>

<style scoped>
.demand-operate {
  float: right;
  padding-bottom: 1rem;
  padding-top: 1rem;
}
</style>