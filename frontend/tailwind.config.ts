import type { Config } from "tailwindcss";

const config: Config = {
    darkMode: ["class"],
    content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
    "*.{js,ts,jsx,tsx,mdx}"
  ],
  theme: {
  	extend: {
  		colors: {
  			// TodoAstros Premium Palette
  			background: 'hsl(var(--background))',
  			foreground: 'hsl(var(--foreground))',
  			
  			// Primary colors
  			primary: {
  				DEFAULT: 'hsl(var(--primary))',
  				foreground: 'hsl(var(--primary-foreground))',
  				dark: '#1a1a2e',
  				navy: '#16213e',
  			},
  			
  			// Secondary
  			secondary: {
  				DEFAULT: 'hsl(var(--secondary))',
  				foreground: 'hsl(var(--secondary-foreground))'
  			},
  			
  			// Accent - Coral red
  			accent: {
  				DEFAULT: 'hsl(var(--accent))',
  				foreground: 'hsl(var(--accent-foreground))',
  				coral: '#e94560',
  			},
  			
  			// Gold theme
  			gold: {
  				DEFAULT: '#d4af37',
  				light: '#f5d67a',
  				dark: '#b8962e',
  				muted: 'rgba(212, 175, 55, 0.2)',
  			},
  			
  			// Zodiac elements
  			zodiac: {
  				fire: '#ff6b6b',
  				earth: '#4ecdc4',
  				air: '#95e1d3',
  				water: '#6c5ce7',
  			},
  			
  			// UI components
  			card: {
  				DEFAULT: 'hsl(var(--card))',
  				foreground: 'hsl(var(--card-foreground))'
  			},
  			popover: {
  				DEFAULT: 'hsl(var(--popover))',
  				foreground: 'hsl(var(--popover-foreground))'
  			},
  			muted: {
  				DEFAULT: 'hsl(var(--muted))',
  				foreground: 'hsl(var(--muted-foreground))'
  			},
  			destructive: {
  				DEFAULT: 'hsl(var(--destructive))',
  				foreground: 'hsl(var(--destructive-foreground))'
  			},
  			border: 'hsl(var(--border))',
  			input: 'hsl(var(--input))',
  			ring: 'hsl(var(--ring))',
  			
  			// Chart colors
  			chart: {
  				'1': 'hsl(var(--chart-fire))',
  				'2': 'hsl(var(--chart-earth))',
  				'3': 'hsl(var(--chart-air))',
  				'4': 'hsl(var(--chart-water))',
  				'5': 'hsl(var(--chart-5))',
  				fire: '#ff6b6b',
  				earth: '#4ecdc4',
  				air: '#95e1d3',
  				water: '#6c5ce7',
  			},
  			
  			// Sidebar
  			sidebar: {
  				DEFAULT: 'hsl(var(--sidebar-background))',
  				foreground: 'hsl(var(--sidebar-foreground))',
  				primary: 'hsl(var(--sidebar-primary))',
  				'primary-foreground': 'hsl(var(--sidebar-primary-foreground))',
  				accent: 'hsl(var(--sidebar-accent))',
  				'accent-foreground': 'hsl(var(--sidebar-accent-foreground))',
  				border: 'hsl(var(--sidebar-border))',
  				ring: 'hsl(var(--sidebar-ring))'
  			}
  		},
  		
  		fontFamily: {
  			display: ['Playfair Display', 'Georgia', 'serif'],
  			sans: ['Inter', 'Arial', 'sans-serif'],
  		},
  		
  		borderRadius: {
  			lg: 'var(--radius)',
  			md: 'calc(var(--radius) - 2px)',
  			sm: 'calc(var(--radius) - 4px)'
  		},
  		
  		boxShadow: {
  			'elegant': '0 4px 20px rgba(26, 26, 46, 0.15), 0 1px 3px rgba(26, 26, 46, 0.1)',
  			'elegant-lg': '0 8px 40px rgba(26, 26, 46, 0.2)',
  			'gold': '0 4px 15px rgba(212, 175, 55, 0.3)',
  			'gold-lg': '0 8px 30px rgba(212, 175, 55, 0.4)',
  		},
  		
  		backgroundImage: {
  			'gradient-gold': 'linear-gradient(135deg, #d4af37 0%, #f5d67a 50%, #d4af37 100%)',
  			'gradient-dark': 'linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #1a1a2e 100%)',
  			'gradient-radial': 'radial-gradient(circle, var(--tw-gradient-stops))',
  		},
  		
  		keyframes: {
  			'accordion-down': {
  				from: { height: '0' },
  				to: { height: 'var(--radix-accordion-content-height)' }
  			},
  			'accordion-up': {
  				from: { height: 'var(--radix-accordion-content-height)' },
  				to: { height: '0' }
  			},
  			'float': {
  				'0%, 100%': { transform: 'translateY(0) rotate(0deg)' },
  				'50%': { transform: 'translateY(-10px) rotate(5deg)' }
  			},
  			'pulse-gold': {
  				'0%, 100%': { boxShadow: '0 0 0 0 rgba(212, 175, 55, 0.4)' },
  				'50%': { boxShadow: '0 0 0 10px rgba(212, 175, 55, 0)' }
  			},
  			'shimmer': {
  				'0%': { backgroundPosition: '-200% 0' },
  				'100%': { backgroundPosition: '200% 0' }
  			}
  		},
  		animation: {
  			'accordion-down': 'accordion-down 0.2s ease-out',
  			'accordion-up': 'accordion-up 0.2s ease-out',
  			'float': 'float 3s ease-in-out infinite',
  			'pulse-gold': 'pulse-gold 2s ease-in-out infinite',
  			'shimmer': 'shimmer 2s linear infinite',
  		}
  	}
  },
  plugins: [require("tailwindcss-animate")],
};

export default config;
