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
          </el-card>
        </div>
      </el-col>
    </el-row>
    <!-- 页面底部加载更多按钮 -->
    <div class="load-more-btn">
      <el-button type="text" @click="load_more">加载更多</el-button>
    </div>

    <!-- 详细信息drawer -->
    <el-drawer
      :title="demand_info.publisher + '所需物资详情'"
      :visible.sync="info_drawer_visible"
      size="40%"
    >
      <div class="base-info">
        <div class="base-info-hospital">{{demand_info.publisher}}</div>
        <div class="base-info-address">
          <div>邮寄地址</div>
          <br />
          {{demand_info.address}}
        </div>
        <div class="base-info-contact">
          <div>联系方式</div>
          <br />
          {{demand_info.phone}}
        </div>
      </div>
      <div class="supply-info">
        <el-table :data="demand_info.supplies">
          <el-table-column prop="name" label="需求物资名称" min-width="35%"></el-table-column>
          <el-table-column prop="specification" label="规格" min-width="55%"></el-table-column>
          <el-table-column prop="number" label="数量" min-width="10%"></el-table-column>
        </el-table>
      </div>
    </el-drawer>

    <!-- 捐赠dialog -->
    <el-dialog
      :title="'向' + donation_info.publisher + '捐赠'"
      :visible.sync="donation_dialog_visible"
      v-loading="is_loading"
    >
      <!-- 捐赠表单 -->
      <el-form :model="donation_info" label-position="left" label-width="25%">
        <el-form-item
          v-for="(supply, index) in donation_info.supplies"
          :key="index"
          :label="supply.name"
        >
          <el-input v-model="supply.specification" placeholder="规格" class="donation-specification"></el-input>
          <el-input v-model="supply.number" placeholder="数量" class="donation-number"></el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-input
          v-model="donation_info.express_code"
          placeholder="请输入快递单号"
          style="width:50%;margin-right:1rem"
        ></el-input>
        <el-button type="success" @click="do_donate">捐赠</el-button>
      </div>
    </el-dialog>
  </el-main>
</template>

<script>
export default {
  data() {
    return {
      demands: [],
      is_loading: false,
      demand_info: {},
      donation_info: {},
      info_drawer_visible: false,
      donation_dialog_visible: false
    };
  },

  // 父组件传值
  props: ["logged_user_info"],

  created() {
    this.get_demands({ page: 0, num: 12 });
  },

  methods: {
    get_demands(params) {
      this.is_loading = true;
      // 处理请求参数
      this.$http.get("/demands", { params: params }).then(
        res => {
          if (res.data.code === 200) {
            this.is_loading = false;
            if (res.data.data !== 0) {
              res.data.data.forEach(demand => {
                this.demands.push(demand);
              });
            }
            if (JSON.stringify(res.data.data) === "[]") {
              this.is_loading = false;
              this.$message.warning("没有更多了");
            }
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
      let params = { page: Math.ceil(this.demands.length / 12), num: 12 };
      this.get_demands(params);
    },
    // 打开详情drawer
    open_demand_info(id) {
      this.info_drawer_visible = true;
      this.demand_info = JSON.parse(JSON.stringify(this.demands[id]));
    },
    // 打开捐赠dialog
    open_donation_dialog(id) {
      if (!this.logged_user_info) {
        this.$router.push("/login");
        this.$message.warning("请先登录");
      }
      this.donation_dialog_visible = true;
      let tmp = JSON.parse(JSON.stringify(this.demands[id]));
      tmp.supplies.forEach(s => {
        s.number = 0;
      });
      this.donation_info = tmp;
    },
    // 发起捐赠请求
    do_donate() {
      this.is_loading = true;
      this.donation_info.donor = this.logged_user_info.id;
      console.log(this.donation_info);
      this.$http.post("/donations", this.donation_info);
      setTimeout(() => {
        this.is_loading = false;
      }, 1000);
    },
    // 拆分地址
    address_split(address) {
      if (address !== null) {
        return (
          address.split("省")[0] + " " + address.split("省")[1].split("市")[0]
        );
      }
    }
  }
};
</script>

<style scoped>
.card-box {
  margin-bottom: 1.25rem;
}

.card-title {
  margin-bottom: 1rem;
}

.card-title > .hospital-name {
  font-size: 1.75rem;
}

.card-address {
  margin-top: 1rem;
  color: #828282;
}

.card-content {
  text-overflow: ellipsis;
  overflow: hidden;
  height: 7rem;
  max-height: 7rem;
  min-height: 7rem;
}

.review-tag {
  margin-left: 1rem;
}

.load-more-btn {
  text-align: center;
}

.supply-name {
  display: inline-block;
}

.supply-number {
  float: right;
}

.supply-item {
  margin-bottom: 1.2rem;
}

.other-supply-num {
  color: #828282;
}

.demand-info-btn {
  text-align: center;
}

.donate-btn {
  text-align: end;
}

.base-info-hospital {
  font-size: 2rem;
  text-align: center;
  margin-bottom: 1rem;
}

.base-info-address {
  width: 50%;
  float: left;
  text-align: center;
  color: #828282;
  margin-bottom: 1rem;
}

.base-info-contact {
  width: 50%;
  float: left;
  text-align: center;
  color: #828282;
  margin-bottom: 1rem;
}

.donation-name {
  width: 20%;
  margin-left: 5%;
}

.donation-specification {
  width: 70%;
  margin-left: 1%;
}

.donation-number {
  width: 20%;
  margin-left: 5%;
}

.donation-remove-btn {
  margin-left: 1%;
}
</style>