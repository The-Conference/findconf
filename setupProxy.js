const { createProxyMiddleware } = require("http-proxy-middleware");

module.exports = function (app) {
  app.use(
    "/api",
    createProxyMiddleware({
      target: "http://test.theconf.ru:8000/",
      changeOrigin: true,
    })
  );
};
