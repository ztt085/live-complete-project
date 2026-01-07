// admin/db.js（模拟数据库模块，适配gateway.js调用）
const db = {
  // 直播流数据（支持getAll、getById、getActive）
  streams: {
    getAll() {
      // 返回模拟的直播流列表（与gateway.js中stream管理逻辑匹配）
      return [
        {
          id: 'stream-1',
          name: '测试HLS直播流',
          url: 'https://test-streams.mux.dev/x36xhzz/x36xhzz.m3u8',
          type: 'hls',
          enabled: true,
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString()
        },
        {
          id: 'stream-2',
          name: '备用RTMP直播流',
          url: 'rtmp://localhost/live/stream2',
          type: 'rtmp',
          enabled: false,
          createdAt: new Date().toISOString(),
          updatedAt: new Date().toISOString()
        }
      ];
    },
    getById(id) {
      // 根据ID查询直播流（适配gateway.js中streamId参数）
      return this.getAll().find(stream => stream.id === id);
    },
    getActive() {
      // 获取启用的直播流（适配gateway.js中start直播逻辑）
      return this.getAll().find(stream => stream.enabled);
    },
    add(newStream) { /* 模拟添加逻辑，适配admin API */
      return {
        ...newStream,
        id: `stream-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`, // 生成唯一ID
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      };
      },
    update(streamId, updates) {
      const stream = this.getById(streamId);
      return { ...stream, ...updates, updatedAt: new Date().toISOString() };
    },
    //update() { /* 模拟更新逻辑，适配admin API */ return {}; },
    delete() { /* 模拟删除逻辑，适配admin API */ }
  },
  // 辩论数据（支持get、update）
  debate: {
    get() {
      // 返回模拟辩题（与gateway.js中debate管理逻辑匹配）
      return {
        title: "如果有一个能一键消除痛苦的按钮，你会按吗？",
        leftPosition: "正方：不按，痛苦促进成长",
        rightPosition: "反方：按，减少无意义痛苦",
        description: "关于痛苦与成长的深度辩论"
      };
    },
    update(data) { /* 模拟更新逻辑，适配admin API */
      const original = this.get();
      return { ...original, ...data, updatedAt: new Date().toISOString() };//return {};
    }
  },
  // 用户数据（支持getAll、getById、createOrUpdate、updateStats）
  users: {
    getAll() {
      // 返回模拟用户列表（适配admin用户管理API）
      return [
        {
          id: 'user-1',
          nickName: '测试用户',
          avatarUrl: '/static/logo.png',
          createdAt: new Date().toISOString(),
          statistics: { totalVotes: 100 }
        }
      ];
    },
    getById(id) {
      // 根据ID查询用户（适配admin用户详情API）
      return this.getAll().find(user => user.id === id);
    },
    createOrUpdate(user) {
      // 模拟创建/更新用户（适配微信登录逻辑）
      return user;
    },
    updateStats(userId, stats) {
      // 模拟更新用户统计（适配投票统计逻辑）
      return { userId, stats };
    }
  },
  // 统计数据（支持get、getDashboard、incrementVotes、updateDashboard）
  statistics: {
    get() {
      // 返回模拟统计数据（适配admin统计API）
      return { totalVotes: 0, dailyStats: [] };
    },
    getDashboard() {
      // 返回模拟仪表盘数据（适配WebSocket广播逻辑）
      return { isLive: false };
    },
    incrementVotes(count) {
      // 模拟票数统计（适配用户投票逻辑）
      return count;
    },
    updateDashboard(data) {
      // 模拟仪表盘更新（适配直播统计逻辑）
      return data;
    }
  },
  // 直播计划（支持get、update、clear）
  liveSchedule: {
    get() {
      // 返回模拟直播计划（适配定时直播逻辑）
      return { isScheduled: false, scheduledStartTime: null };
    },
    update(schedule) {
      // 模拟更新直播计划（适配admin计划设置API）
      return schedule;
    },
    clear() {
      // 模拟清除直播计划（适配停止直播逻辑）
      return true;
    }
  }
};

module.exports = db; // 导出db模块，供gateway.js引入