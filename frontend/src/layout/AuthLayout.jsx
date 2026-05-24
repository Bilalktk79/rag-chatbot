import { Outlet } from "react-router-dom";

const AuthLayout = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-900 via-purple-900 to-black">
      
      {/* CENTERED CARD WRAPPER */}
      <div className="w-full max-w-5xl h-[550px]">
        <Outlet />
      </div>

    </div>
  );
};

export default AuthLayout;