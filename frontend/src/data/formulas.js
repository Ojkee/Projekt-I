const formulas = [
  {
    category: "Algebra",
    items: [
      {
        name: "Quadratic Equation",
        latex: [
          "x_1 = \\frac{-b - \\sqrt{b^2 - 4ac}}{2a}",
          "x_2 = \\frac{-b + \\sqrt{b^2 - 4ac}}{2a}",
        ],
      },
      {
        name: "Discriminant (Delta)",
        latex: "\\Delta = b^2 - 4ac",
      },
      {
        name: "Sum and Product of Roots",
        latex: [
          "x_1 + x_2 = -\\frac{b}{a}",
          "\\quad x_1 x_2 = \\frac{c}{a}",
        ],
      },
      {
        name: "Binomial Identities",
        latex: [
          "(a+b)^2 = a^2 + 2ab + b^2",
          "(a-b)^2 = a^2 - 2ab + b^2",
          "a^2 - b^2 = (a-b)(a+b)",
          "(a+b)^3 = a^3 + 3a^2b + 3ab^2 + b^3",
          "(a-b)^3 = a^3 - 3a^2b + 3ab^2 - b^3",
        ],
      },
      {
        name: "Logarithms",
        latex: [
          "\\log_a(xy) = \\log_a x + \\log_a y",
          "\\log_a(x/y) = \\log_a x - \\log_a y",
          "\\log_a x^n = n \\log_a x",
        ],
      },
      {
        name: "Sequences",
        latex: [
          "a_n = a_1 + (n-1)d",
          "S_n = \\frac{n(a_1 + a_n)}{2}",
          "a_n = a_1 r^{n-1}",
          "S_n = a_1 \\frac{1-r^n}{1-r}, r \\neq 1",
        ],
      },
      {
        name: "Product of Powers",
        latex: [
          { eq_name: "!product_of_powers", eq: "a^r \\cdot a^s = a^{r + s}" },
        ],
      },
    ],
  },
  {
    category: "Trigonometry",
    items: [
      {
        name: "Basic Identities",
        latex: [
          "\\sin^2 x + \\cos^2 x = 1",
          "\\tan x = \\frac{\\sin x}{\\cos x}",
          "\\cot x = \\frac{\\cos x}{\\sin x}",
        ],
      },
      {
        name: "Reduction Formulas",
        latex: [
          "\\sin(-x) = -\\sin x",
          "\\cos(-x) = \\cos x",
          "\\sin(\\pi - x) = \\sin x",
          "\\cos(\\pi - x) = -\\cos x",
        ],
      },
      {
        name: "Sum and Difference Formulas",
        latex: [
          "\\sin(a \\pm b) = \\sin a \\cos b \\pm \\cos a \\sin b",
          "\\cos(a \\pm b) = \\cos a \\cos b \\mp \\sin a \\sin b",
          "\\tan(a \\pm b) = \\frac{\\tan a \\pm \\tan b}{1 \\mp \\tan a \\tan b}",
        ],
      },
      {
        name: "Double Angle Formulas",
        latex: [
          "\\sin 2x = 2 \\sin x \\cos x",
          "\\cos 2x = \\cos^2 x - \\sin^2 x",
          "\\tan 2x = \\frac{2 \\tan x}{1 - \\tan^2 x}",
        ],
      },
    ],
  },
  {
    category: "Geometry",
    items: [
      {
        name: "Pythagorean Theorem",
        latex: "a^2 + b^2 = c^2",
      },
      {
        name: "Area of a Circle",
        latex: "S = \\pi r^2",
      },
      {
        name: "Circumference of a Circle",
        latex: "C = 2\\pi r",
      },
      {
        name: "Volume of Solids",
        latex: [
          "V_{cube} = a^3",
          "V_{cuboid} = a b c",
          "V_{cone} = \\frac{1}{3} \\pi r^2 h",
          "V_{cylinder} = \\pi r^2 h",
          "V_{sphere} = \\frac{4}{3} \\pi r^3",
        ],
      },
    ],
  },
  {
    category: "Calculus",
    items: [
      {
        name: "Derivative",
        latex: "f'(x) = \\lim_{h \\to 0} \\frac{f(x+h)-f(x)}{h}",
      },
      {
        name: "Indefinite Integral",
        latex: "\\int f(x) dx",
      },
      {
        name: "Limit of a Function",
        latex: "\\lim_{x \\to a} f(x)",
      },
    ],
  },
  {
    category: "Combinatorics and Statistics",
    items: [
      {
        name: "Permutations",
        latex: "P_n = n!",
      },
      {
        name: "Combinations",
        latex: "C_n^k = \\frac{n!}{k!(n-k)!}",
      },
      {
        name: "Mean and Variance",
        latex: [
          "\\bar{x} = \\frac{\\sum x_i}{n}",
          "\\sigma^2 = \\frac{\\sum (x_i - \\bar{x})^2}{n}",
        ],
      },
    ],
  },
];

export default formulas;
