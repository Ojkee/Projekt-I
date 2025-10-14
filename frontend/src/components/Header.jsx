import { motion } from "framer-motion";
import { Sparkles } from "lucide-react";

function Header() {
  return (
    <>
      <motion.div
        initial={{ scale: 0, rotate: -180 }}
        animate={{ scale: 1, rotate: 0 }}
        transition={{ delay: 0.2, duration: 0.6, type: "spring", stiffness: 200 }}
        className="p-4 bg-gradient-to-br from-blue-500 to-purple-600 rounded-2xl shadow-lg"
      >
        <Sparkles className="w-8 h-8 text-white" />
      </motion.div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4, duration: 0.6 }}
        className="w-full"
      >
        <h1 className="text-4xl sm:text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent mb-4 leading-[1.2] tracking-tight">
          Witaj w Matice
        </h1>
        <p className="text-lg text-gray-700 leading-relaxed mt-4 px-2 font-medium">
          Odkryj nowe możliwości i rozpocznij swoją podróż. Kliknij poniżej, aby przejść dalej.
        </p>
      </motion.div>
    </>
  );
}

export default Header;
