import react from '@vitejs/plugin-react'
import vike from 'vike/plugin'
import { UserConfig } from 'vite'

const config: UserConfig = {
  plugins: [
    react(),
    vike({ prerender: true })
  ],
  ssr: {
    noExternal: ["styled-components", "@emotion/*"],
  },
}

export default config
