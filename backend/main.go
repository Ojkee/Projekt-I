package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/cors"
)

func runDev(r *chi.Mux) {
	r.Use(cors.Handler(cors.Options{
		AllowedOrigins:   []string{"http://localhost:5173"},
		AllowedMethods:   []string{"GET", "POST", "OPTIONS"},
		AllowedHeaders:   []string{"Content-Type"},
		AllowCredentials: true,
	}))
}

func runProd(r *chi.Mux) {
	distPath := "../frontend/dist"

	if _, err := os.Stat(distPath); err == nil {
		fs := http.FileServer(http.Dir(distPath))
		r.Handle("/*", fs)
	}
}

func main() {
	r := chi.NewRouter()

	args := os.Args[1:]
	if len(args) > 1 {
		fmt.Println("error: too many arguments, use 'dev' or 'prod'")
		os.Exit(1)
	}

	mode := "dev" // default mode
	if len(args) > 0 {
		mode = args[0]
		fmt.Println("Run in mode: ", mode)
	}

	switch mode {
	case "dev":
		fmt.Println("Developer mode enabled")
		runDev(r)
	case "prod":
		fmt.Println("Production mode enabled")
		runProd(r)
	default:
		fmt.Println("error: unknown type, use 'dev' or 'prod'")
		os.Exit(1)
	}

	r.Post("/hello", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "application/json")
		json.NewEncoder(w).Encode(map[string]string{
			"message": "Hello World from Go!",
		})
	})

	if err := http.ListenAndServe(":8080", r); err != nil {
		fmt.Printf("Server error: %v\n", err)
	}
}
