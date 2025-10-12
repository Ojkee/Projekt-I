import { motion } from "framer-motion";
import Background from "../components/Background";
import Header from "../components/Header";
import StartButton from "../components/StartButton";

function HomePage() {
  return (
    <div className="min-h-screen flex items-center justify-center p-4 relative overflow-hidden">
      <Background />
      
      <motion.div
        initial={{ opacity: 0, y: 50, scale: 0.9 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        transition={{ duration: 0.8, ease: "easeOut" }}
        className="relative z-10 flex flex-col items-center text-center gap-8 p-10 sm:p-12 bg-white/80 backdrop-blur-xl rounded-3xl shadow-2xl border border-white/20 max-w-md w-full font-['Inter']"
      >
        <Header />
        <StartButton />
      </motion.div>
    </div>
  );
}

export default HomePage;
