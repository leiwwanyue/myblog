const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000', // Django 后端的地址
        changeOrigin: true,
        pathRewrite: { '^/api': '' }, // 将 /api 前缀移除
      },
    },
  },
  outputDir: '../static/vue',
})
