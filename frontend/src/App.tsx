import { Routes, Route, Navigate } from "react-router-dom";
import { LoginPage } from "./pages/LoginPage";
import { RegisterPage } from "./pages/RegisterPage";
import ChatInterface from "./ChatInterface"; // 导入我们刚刚创建的聊天界面

/**
 * 这是一个受保护的路由组件。
 * 它的作用是检查用户是否已登录（通过查看localStorage中是否存在token）。
 * @param children - 如果用户已登录，则渲染这个子组件（例如聊天主页）。
 */
function ProtectedRoute({ children }: { children: JSX.Element }) {
  const token = localStorage.getItem('accessToken');

  if (!token) {
    // 如果在localStorage中找不到token，说明用户未登录，
    // 我们将他重定向到/login页面。`replace`属性可以防止用户通过后退按钮回到受保护的页面。
    return <Navigate to="/login" replace />;
  }

  // 如果token存在，就正常渲染子组件。
  return children;
}

/**
 * 这是应用的根组件，现在它的唯一职责就是定义路由规则。
 */
export default function App() {
  return (
    <Routes>
      {/* 公开路由：任何人都可以访问 */}
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />

      {/* 受保护的路由：只有登录用户才能访问。
        我们将ChatInterface组件包裹在ProtectedRoute中。
      */}
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <ChatInterface />
          </ProtectedRoute>
        }
      />

      {/* 这是一个备用/捕获所有路由。如果用户访问了任何未定义的路径，
        例如 /some/random/path，它会自动将用户重定向回主页 (/)。
      */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}