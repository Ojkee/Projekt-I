const formulas = [
  {
    category: "Algebra",
    items: [
      {
        name: "Równanie kwadratowe",
        latex: ["x_1 = \\frac{-b - \\sqrt{b^2 - 4ac}}{2a}",
          "x_2 = \\frac{-b + \\sqrt{b^2 - 4ac}}{2a}",
        ]
      },
      {
        name: "Delta",
        latex: "\\Delta = b^2 - 4ac",
      },
      {
        name: "Suma i iloczyn pierwiastków",
        latex: [
          "x_1 + x_2 = -\\frac{b}{a}", 
          "\\quad x_1 x_2 = \\frac{c}{a}",
        ]
      },
      {
        name: "Wzory skróconego mnożenia",
        latex: [
          "(a+b)^2 = a^2 + 2ab + b^2",
          "(a-b)^2 = a^2 - 2ab + b^2",
          "a^2 - b^2 = (a-b)(a+b)",
          "(a+b)^3 = a^3 + 3a^2b + 3ab^2 + b^3",
          "(a-b)^3 = a^3 - 3a^2b + 3ab^2 - b^3",
        ],
      },
      {
        name: "Logarytmy",
        latex: [
          "\\log_a(xy) = \\log_a x + \\log_a y",
          "\\log_a(x/y) = \\log_a x - \\log_a y",
          "\\log_a x^n = n \\log_a x",
        ],
      },
      {
        name: "Ciągi",
        latex: [
          "a_n = a_1 + (n-1)d",
          "S_n = \\frac{n(a_1 + a_n)}{2}",
          "a_n = a_1 r^{n-1}",
          "S_n = a_1 \\frac{1-r^n}{1-r}, r \\neq 1",
        ],
      },
    ],
  },
  {
    category: "Trygonometria",
    items: [
      {
        name: "Podstawowe tożsamości",
        latex: [
          "\\sin^2 x + \\cos^2 x = 1",
          "\\tan x = \\frac{\\sin x}{\\cos x}",
          "\\cot x = \\frac{\\cos x}{\\sin x}",
        ],
      },
      {
        name: "Wzory redukcyjne",
        latex: [
          "\\sin(-x) = -\\sin x",
          "\\cos(-x) = \\cos x",
          "\\sin(\\pi - x) = \\sin x",
          "\\cos(\\pi - x) = -\\cos x",
        ],
      },
      {
        name: "Wzory na sumę i różnicę kątów",
        latex: [
          "\\sin(a \\pm b) = \\sin a \\cos b \\pm \\cos a \\sin b",
          "\\cos(a \\pm b) = \\cos a \\cos b \\mp \\sin a \\sin b",
          "\\tan(a \\pm b) = \\frac{\\tan a \\pm \\tan b}{1 \\mp \\tan a \\tan b}",
        ],
      },
      {
        name: "Wzory podwójnego kąta",
        latex: [
          "\\sin 2x = 2 \\sin x \\cos x",
          "\\cos 2x = \\cos^2 x - \\sin^2 x",
          "\\tan 2x = \\frac{2 \\tan x}{1 - \\tan^2 x}",
        ],
      },
    ],
  },
  {
    category: "Geometria",
    items: [
      {
        name: "Twierdzenie Pitagorasa",
        latex: "a^2 + b^2 = c^2",
      },
      {
        name: "Pole trójkąta (Herona)",
        latex: "S = \\sqrt{p(p-a)(p-b)(p-c)}, \\quad p = \\frac{a+b+c}{2}",
      },
      {
        name: "Pole koła",
        latex: "S = \\pi r^2",
      },
      {
        name: "Obwód koła",
        latex: "C = 2\\pi r",
      },
      {
        name: "Objętość brył",
        latex: [
          "V_{sześcian} = a^3",
          "V_{prostopadłościan} = a b c",
          "V_{stożek} = \\frac{1}{3} \\pi r^2 h",
          "V_{walec} = \\pi r^2 h",
          "V_{kula} = \\frac{4}{3} \\pi r^3",
        ],
      },
    ],
  },
  {
    category: "Analiza",
    items: [
      {
        name: "Pochodna",
        latex: "f'(x) = \\lim_{h \\to 0} \\frac{f(x+h)-f(x)}{h}",
      },
      {
        name: "Całka nieoznaczona",
        latex: "\\int f(x) dx",
      },
      {
        name: "Granica funkcji",
        latex: "\\lim_{x \\to a} f(x)",
      },
    ],
  },
  {
    category: "Kombinatoryka i Statystyka",
    items: [
      {
        name: "Permutacje",
        latex: "P_n = n!",
      },
      {
        name: "Kombinacje",
        latex: "C_n^k = \\frac{n!}{k!(n-k)!}",
      },
      {
        name: "Prawdopodobieństwo zdarzenia",
        latex:
          "P(A) = \\frac{liczba\\ zdarzeń\\ sprzyjających}{liczba\\ zdarzeń\\ możliwych}",
      },
      {
        name: "Średnia i wariancja",
        latex: [
          "\\bar{x} = \\frac{\\sum x_i}{n}",
          "\\sigma^2 = \\frac{\\sum (x_i - \\bar{x})^2}{n}",
        ],
      },
    ],
  },
];

export default formulas;
