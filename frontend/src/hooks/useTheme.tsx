import { createContext, useContext, useState, useEffect, ReactNode } from 'react'


type Theme = 'dark' | 'light'


interface ThemeContextType {
  theme: Theme
  toggleTheme: () => void
}


const ThemeContext = createContext<ThemeContextType | undefined>(undefined)


export function ThemeProvider({ children }: { children: ReactNode }) {

  const [theme, setTheme] = useState<Theme>('dark')


  const toggleTheme = () => {
    setTheme(prev => prev === 'dark' ? 'light' : 'dark')
  }


  useEffect(() => {

    document.documentElement.classList.remove(
      'dark',
      'light'
    )

    document.documentElement.classList.add(theme)

  }, [theme])


  return (
    <ThemeContext.Provider
      value={{
        theme,
        toggleTheme
      }}
    >
      {children}
    </ThemeContext.Provider>
  )
}


export function useTheme() {

  const context = useContext(
    ThemeContext
  )


  if (context === undefined) {
    throw new Error(
      'useTheme must be used within a ThemeProvider'
    )
  }


  return context
}