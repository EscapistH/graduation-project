<template>
  <el-main v-loading="is_loading">
    <!-- 行 -->
    <el-row :gutter="12" v-for="(each_row, index) in Math.ceil(demands.length/4)" :key="index">
      <!-- 列 -->
      <div v-if="demands.length === 0" style="text-align:center;">再怎么找也没有啦</div>
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
            <!-- 卡片头部 -->
            <div slot="header" class="card-header">
              <!-- 卡片标题 -->
              <span class="demand-title">{{demand.title}}</span>
              <!-- tag 是否验证 -->
              <el-tag
                :type="demand.is_review===true?'success':'warning'"
                size="mini"
                effect="dark"
                class="review-tag"
              >{{demand.is_review===true?'已验证':'未验证'}}</el-tag>
              <el-tag type="danger" size="mini" effect="dark" class="review-tag">已撤销</el-tag>
              <br />
              <!-- 发布时间 -->
              <span class="demand-pub-time">发布时间: {{demand.pub_time}}</span>
            </div>
            <!-- 卡片主体 -->
            <div class="card-content">
              <el-table :data="demand.content">
                <el-table-column label="需求物资" prop="name"></el-table-column>
                <el-table-column label="需求数量" prop="num"></el-table-column>
              </el-table>
            </div>
            <div class="demand-publisher">
              <span>联系人: {{demand.publisher}}</span>
              <br />
              <span>联系电话: {{demand.phone}}</span>
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
      params: { page: 0, num: 12 },
      is_loading_more: false
    };
  },
  created() {
    this.get_some_demands();
  },
  methods: {
    get_some_demands() {
      this.is_loading = true;
      this.$http.get("/my_cancel_demands", { params: this.params }).then(
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
      this.$http.get("/my_cancel_demands", { params: this.params }).then(
        res => {
          // console.log(res);
          if (res.data.code === 200) {
            this.is_loading_more = false;
            if (res.data.data.length === 0)
              return this.$message.warning("没有更多了");
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
    }
  }
};
</script>

<style scoped>
</style>