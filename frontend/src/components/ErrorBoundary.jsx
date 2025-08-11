import React from 'react'

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props)
    this.state = { hasError: false, error: null }
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error }
  }

  componentDidCatch(error, info) {
    // Log for debugging
    console.error('ErrorBoundary caught an error:', error, info)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: 24 }} className="min-h-screen bg-black text-white">
          <h1 className="text-2xl font-bold mb-2">Something went wrong.</h1>
          <p className="opacity-80">A runtime error occurred in the UI. Check the console for details.</p>
          {process.env.NODE_ENV !== 'production' && this.state.error && (
            <pre className="mt-4 p-3 rounded bg-white/10 overflow-auto">
              {String(this.state.error?.message || this.state.error)}
            </pre>
          )}
        </div>
      )
    }
    return this.props.children
  }
}

export default ErrorBoundary
