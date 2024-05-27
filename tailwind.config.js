/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html", // すべてのHTMLテンプレートファイル
    "./**/*.py", // すべてのPythonファイル
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
