import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import api from '../api/axios'

// Allauth URL для социальных сетей
// i18n_patterns добавляет /ru/ префикс
const SOCIAL = {
  google: '/ru/accounts/google/login/',
  github: '/ru/accounts/github/login/',
}

function LoginPage() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [focused, setFocused] = useState(null)

  const handleLogin = async () => {
    if (!email || !password) { setError('Заполните все поля'); return }
    setError(''); setLoading(true)
    try {
      const res = await api.post('/login/', { email, password })
      localStorage.setItem('access_token', res.data.access)
      localStorage.setItem('refresh_token', res.data.refresh)
      navigate('/')
      window.location.reload()
    } catch (err) {
      // Показываем конкретную ошибку от сервера
      const data = err.response?.data
      if (data?.email) setError(Array.isArray(data.email) ? data.email[0] : data.email)
      else if (data?.password) setError(Array.isArray(data.password) ? data.password[0] : data.password)
      else if (data?.non_field_errors) setError(data.non_field_errors[0])
      else if (data?.detail) setError(data.detail)
      else setError('Неверный email или пароль')
    } finally { setLoading(false) }
  }

  const inp = (f) => ({
    ...styles.input,
    ...(focused === f ? styles.inputFocused : {}),
  })

  return (
    <div style={styles.page}>
      <div style={styles.blob1} />
      <div style={styles.blob2} />

      <div style={styles.card}>
        <div style={styles.topLine} />

        {/* Шапка */}
        <div style={styles.header}>
          <div style={styles.logoBox}>
            <span style={styles.logoLetter}>А</span>
          </div>
          <div>
            <h1 style={styles.title}>Авито</h1>
            <p style={styles.subtitle}>Войдите в аккаунт</p>
          </div>
        </div>

        {/* Ошибка */}
        {error && <div style={styles.errorBox}>⚠️ &nbsp;{error}</div>}

        {/* Поля */}
        <div style={styles.fields}>
          <div style={styles.field}>
            <label style={styles.label}>Электронная почта</label>
            <input
              style={inp('email')} type='email' placeholder='admin@admin.com'
              value={email} onChange={(e) => setEmail(e.target.value)}
              onFocus={() => setFocused('email')} onBlur={() => setFocused(null)}
              onKeyDown={(e) => e.key === 'Enter' && handleLogin()}
            />
          </div>
          <div style={styles.field}>
            <label style={styles.label}>Пароль</label>
            <input
              style={inp('password')} type='password' placeholder='••••••••'
              value={password} onChange={(e) => setPassword(e.target.value)}
              onFocus={() => setFocused('password')} onBlur={() => setFocused(null)}
              onKeyDown={(e) => e.key === 'Enter' && handleLogin()}
            />
          </div>
        </div>

        {/* Кнопка входа */}
        <button
          style={{ ...styles.btn, opacity: loading ? 0.7 : 1 }}
          onClick={handleLogin} disabled={loading}
        >
          {loading ? 'Входим...' : 'Войти →'}
        </button>

        {/* Нет аккаунта */}
        <p style={styles.registerLink}>
          Нет аккаунта?{' '}
          <Link to='/register' style={styles.link}>Зарегистрироваться</Link>
        </p>

        {/* Разделитель */}
        <div style={styles.divider}>
          <div style={styles.dividerLine} />
          <span style={styles.dividerText}>или войти через</span>
          <div style={styles.dividerLine} />
        </div>

        {/* Социальные кнопки */}
        <div style={styles.socialBtns}>
          {/* Google */}
          <a href={SOCIAL.google} style={styles.socialBtn}>
            <svg width='18' height='18' viewBox='0 0 24 24'>
              <path fill='#4285F4' d='M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z'/>
              <path fill='#34A853' d='M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z'/>
              <path fill='#FBBC05' d='M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z'/>
              <path fill='#EA4335' d='M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z'/>
            </svg>
            <span>Google</span>
          </a>

          {/* GitHub */}
          <a href={SOCIAL.github} style={styles.socialBtn}>
            <svg width='18' height='18' viewBox='0 0 24 24' fill='#e0e0f0'>
              <path d='M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z'/>
            </svg>
            <span>GitHub</span>
          </a>
        </div>

        {/* Тестовые аккаунты */}
        <div style={styles.hint}>
          <p style={styles.hintLabel}>Тестовые аккаунты</p>
          {['admin@admin.com', 'user1@admin.com', 'user2@admin.com'].map((e) => (
            <button key={e} style={styles.hintChip}
              onClick={() => { setEmail(e); setPassword('admin') }}>
              {e}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}

const styles = {
  page: {
    minHeight: '90vh', display: 'flex',
    alignItems: 'center', justifyContent: 'center',
    padding: '32px', position: 'relative', overflow: 'hidden',
  },
  blob1: {
    position: 'fixed', top: '5%', left: '20%',
    width: '500px', height: '500px', borderRadius: '50%',
    background: 'radial-gradient(circle, rgba(123,79,255,0.12), transparent 70%)',
    filter: 'blur(40px)', pointerEvents: 'none',
  },
  blob2: {
    position: 'fixed', bottom: '5%', right: '15%',
    width: '400px', height: '400px', borderRadius: '50%',
    background: 'radial-gradient(circle, rgba(59,158,255,0.1), transparent 70%)',
    filter: 'blur(40px)', pointerEvents: 'none',
  },
  card: {
    position: 'relative', width: '100%', maxWidth: '420px',
    background: 'rgba(255,255,255,0.04)',
    backdropFilter: 'blur(24px)', WebkitBackdropFilter: 'blur(24px)',
    border: '1px solid rgba(255,255,255,0.1)',
    borderRadius: '24px', padding: '40px',
    boxShadow: '0 24px 80px rgba(0,0,0,0.4)', overflow: 'hidden',
  },
  topLine: {
    position: 'absolute', top: 0, left: 0, right: 0, height: '2px',
    background: 'linear-gradient(90deg, #7B4FFF, #3B9EFF, #7B4FFF)',
  },
  header: { display: 'flex', alignItems: 'center', gap: '14px', marginBottom: '28px' },
  logoBox: {
    width: '52px', height: '52px', borderRadius: '14px', flexShrink: 0,
    background: 'linear-gradient(135deg, #7B4FFF, #3B9EFF)',
    display: 'flex', alignItems: 'center', justifyContent: 'center',
    boxShadow: '0 8px 24px rgba(123,79,255,0.4)',
  },
  logoLetter: { fontFamily: "'Unbounded', sans-serif", fontSize: '22px', fontWeight: '900', color: '#fff' },
  title: { fontFamily: "'Unbounded', sans-serif", fontSize: '20px', fontWeight: '700', color: '#f0f0f8', margin: '0 0 2px' },
  subtitle: { color: '#555570', fontSize: '13px', margin: 0 },
  errorBox: {
    background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.3)',
    borderRadius: '10px', padding: '12px 16px',
    color: '#fca5a5', fontSize: '14px', marginBottom: '20px',
  },
  fields: { display: 'flex', flexDirection: 'column', gap: '14px', marginBottom: '18px' },
  field: { display: 'flex', flexDirection: 'column', gap: '7px' },
  label: { fontSize: '11px', fontWeight: '600', color: '#555570', textTransform: 'uppercase', letterSpacing: '0.6px' },
  input: {
    background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.08)',
    borderRadius: '12px', padding: '13px 16px',
    color: '#eeeef8', fontSize: '15px', outline: 'none',
    fontFamily: "'Inter', sans-serif", transition: 'all 0.2s',
  },
  inputFocused: { background: 'rgba(123,79,255,0.08)', borderColor: 'rgba(123,79,255,0.5)' },
  btn: {
    width: '100%', padding: '14px',
    background: 'linear-gradient(135deg, #7B4FFF, #3B9EFF)',
    border: 'none', borderRadius: '12px', color: '#fff',
    fontSize: '16px', fontWeight: '700', cursor: 'pointer',
    fontFamily: "'Inter', sans-serif",
    boxShadow: '0 8px 24px rgba(123,79,255,0.3)', marginBottom: '16px',
  },
  registerLink: { textAlign: 'center', color: '#555570', fontSize: '14px', marginBottom: '20px' },
  link: { color: '#a78bff', textDecoration: 'none', fontWeight: '600' },
  divider: { display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '16px' },
  dividerLine: { flex: 1, height: '1px', background: 'rgba(255,255,255,0.08)' },
  dividerText: { color: '#333355', fontSize: '12px', whiteSpace: 'nowrap' },
  socialBtns: { display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', marginBottom: '20px' },
  socialBtn: {
    display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px',
    padding: '11px', borderRadius: '10px', textDecoration: 'none',
    background: 'rgba(255,255,255,0.04)', border: '1px solid rgba(255,255,255,0.08)',
    color: '#e0e0f0', fontSize: '14px', fontWeight: '500',
    fontFamily: "'Inter', sans-serif", transition: 'all 0.2s',
  },
  hint: {
    background: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.06)',
    borderRadius: '12px', padding: '14px',
  },
  hintLabel: {
    fontSize: '11px', fontWeight: '600', color: '#333355',
    textTransform: 'uppercase', letterSpacing: '0.6px', margin: '0 0 8px',
  },
  hintChip: {
    display: 'block', width: '100%', textAlign: 'left',
    background: 'rgba(123,79,255,0.08)', border: '1px solid rgba(123,79,255,0.15)',
    borderRadius: '8px', padding: '7px 12px', color: '#a78bff',
    fontSize: '13px', cursor: 'pointer', fontFamily: 'monospace', marginTop: '5px',
  },
}

export default LoginPage
