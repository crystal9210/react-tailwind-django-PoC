/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html", // すべてのHTMLテンプレートファイル
    "./**/*.py", // すべてのPythonファイル
    "./src/**/*.{js,jsx,ts,tsx}", // すべてのReactコンポーネントファイル
  ],
  theme: {
    extend: {},
  },
  plugins: [],
};
