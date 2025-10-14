import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";

function StartButton() {
  const navigate = useNavigate();

  return (
    <motion.button
      initial={{ opacity: 0, scale: 0 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ delay: 0.6, duration: 0.5, type: "spring", stiffness: 200 }}
      whileHover={{ scale: 1.05, boxShadow: "0 20px 40px rgba(99, 102, 241, 0.3)" }}
      whileTap={{ scale: 0.95 }}
      onClick={() => navigate("/user")}
      className="group relative flex items-center justify-center p-5 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden w-full max-w-[280px] min-h-[60px] font-semibold"
    >
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000" />
      <div className="flex items-center justify-center gap-3 w-full relative">
        <span className="text-lg tracking-wide">Rozpocznij</span>
      </div>
    </motion.button>
  );
}

export default StartButton;
