import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './Auth.css'; // Keep for base styles if any

// Assuming you have an API_URL set up in your environment
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    try {
      const response = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({
          username: email,
          password: password,
        }),
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'Failed to log in');
      }

      const data = await response.json();
      localStorage.setItem('accessToken', data.access_token);

      navigate('/app');

    } catch (err: any) {
      setError(err.message);
    }
  };

  // The UI is now built with Tailwind CSS classes
  return (
    <div className="auth-container flex min-h-screen flex-col items-center justify-center">
      <div className="w-full max-w-md space-y-8 rounded-lg bg-card p-8 shadow-lg">
        <div className="text-center">
          <h2 className="text-3xl font-bold tracking-tight text-card-foreground">
            Log in to your account
          </h2>
        </div>

        <form className="space-y-6" onSubmit={handleSubmit}>
          {error && <p className="rounded-md border border-destructive bg-destructive/10 p-3 text-center text-sm text-destructive">{error}</p>}

          <div className="space-y-2">
            <label htmlFor="email" className="text-sm font-medium text-muted-foreground">
              Email
            </label>
            <input
              id="email"
              name="email"
              type="email"
              autoComplete="email"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              // Using theme variables via CSS classes
              className="block w-full rounded-md border-0 bg-input p-3 text-foreground shadow-sm ring-1 ring-inset ring-ring focus:ring-2 focus:ring-inset"
              placeholder="your@email.com"
            />
          </div>

          <div className="space-y-2">
            <label htmlFor="password" className="text-sm font-medium text-muted-foreground">
              Password
            </label>
            <input
              id="password"
              name="password"
              type="password"
              autoComplete="current-password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="block w-full rounded-md border-0 bg-input p-3 text-foreground shadow-sm ring-1 ring-inset ring-ring focus:ring-2 focus:ring-inset"
              placeholder="Enter your password"
            />
          </div>

          <div>
            <button
              type="submit"
              className="flex w-full justify-center rounded-md bg-primary px-3 py-2 text-sm font-semibold text-primary-foreground shadow-sm hover:bg-primary/90 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2"
            >
              Log In
            </button>
          </div>
        </form>

        <div className="text-center text-sm text-muted-foreground">
          <Link to="/register" className="font-semibold text-primary hover:text-primary/90">
            Don't have an account? Sign up
          </Link>
          <span className="mx-2">|</span>
          <a href="#" className="font-semibold text-primary hover:text-primary/90">
            Forgot password?
          </a>
        </div>
      </div>
    </div>
  );
}