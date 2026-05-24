import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import api from '../api/axios'

function RegisterPage() {
  const navigate = useNavigate()
  const [form, setForm] = useState({
    username: '', email: '', password: '', password2: '', phone_number: '', age: ''
  })
  const [errors, setErrors] = useState({})
  const [loading, setLoading] = useState(false)
  const [focused, setFocused] = useState(null)

  const set = (key, val) => setForm((p) => ({ ...p, [key]: val }))

  const validate = () => {
    const e = {}
    if (!form.username) e.username = 'Введите имя пользователя'
    if (!form.email) e.email = 'Введите email'
    if (!form.password) e.password = 'Введите пароль'
    if (form.password.length < 6) e.password = 'Минимум 6 символов'
    if (form.password !== form.password2) e.password2 = 'Пароли не совпадают'
    if (form.age && (form.age < 17 || form.age > 70)) e.age = 'Возраст от 17 до 70'
    return e
  }

  const handleRegister = async () => {
    const e = validate()
    if (Object.keys(e).length > 0) { setErrors(e); return }
    setErrors({}); setLoading(true)
    try {
      const payload = {
        username: form.username,
        email: form.email,
        password: form.password,
      }
      if (form.phone_number) payload.phone_number = form.phone_number
      if (form.age) payload.age = parseInt(form.age)

      await api.post('/register/', payload)

      // После регистрации сразу логиним
      const res = await api.post('/login/', { email: form.email, password: form.password })
      localStorage.setItem('access_token', res.data.access)
      localStorage.setItem('refresh_token', res.data.refresh)
      navigate('/')
      window.location.reload()
    } catch (err) {
      const data = err.response?.data
      if (data) {
        const mapped = {}
        if (data.email) mapped.email = Array.isArray(data.email) ? data.email[0] : data.email
        if (data.username) mapped.username = Array.isArray(data.username) ? data.username[0] : data.username
        if (data.password) mapped.password = Array.isArray(data.password) ? data.password[0] : data.password
        if (Object.keys(mapped).length > 0) { setErrors(mapped); return }
      }
      setErrors({ general: 'Ошибка регистрации. Попробуй ещё раз.' })
    } finally { setLoading(false) }
  }

  const inp = (field) => ({
    ...styles.input,
    ...(focused === field ? styles.inputFocused : {}),
    ...(errors[field] ? styles.inputError : {}),
  })

  const fields = [
    { key: 'username',     label: 'Имя пользователя',  type: 'text',     placeholder: 'john_doe',          required: true  },
    { key: 'email',        label: 'Email',              type: 'email',    placeholder: 'you@example.com',    required: true  },
    { key: 'password',     label: 'Пароль',             type: 'password', placeholder: '••••••••',           required: true  },
    { key: 'password2',    label: 'Повторите пароль',   type: 'password', placeholder: '••••••••',           required: true  },
    { key: 'phone_number', label: 'Телефон',            type: 'text',     placeholder: '+996 700 123 456',   required: false },
    { key: 'age',          label: 'Возраст',            type: 'number',   placeholder: '25',                 required: false },
  ]

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
            <h1 style={styles.title}>Регистрация</h1>
            <p style={styles.subtitle}>Создайте аккаунт бесплатно</p>
          </div>
        </div>

        {/* Общая ошибка */}
        {errors.general && (
          <div style={styles.errorBox}>⚠️ &nbsp;{errors.general}</div>
        )}

        {/* Поля */}
        <div style={styles.fields}>
          {/* Первый ряд — имя + email */}
          <div style={styles.row}>
            {fields.slice(0, 2).map((f) => (
              <div key={f.key} style={styles.field}>
                <label style={styles.label}>
                  {f.label}
                  {f.required && <span style={styles.req}> *</span>}
                </label>
                <input
                  style={inp(f.key)}
                  type={f.type}
                  placeholder={f.placeholder}
                  value={form[f.key]}
                  onChange={(e) => set(f.key, e.target.value)}
                  onFocus={() => setFocused(f.key)}
                  onBlur={() => setFocused(null)}
                />
                {errors[f.key] && <p style={styles.fieldErr}>⚠ {errors[f.key]}</p>}
              </div>
            ))}
          </div>

          {/* Второй ряд — пароли */}
          <div style={styles.row}>
            {fields.slice(2, 4).map((f) => (
              <div key={f.key} style={styles.field}>
                <label style={styles.label}>
                  {f.label}
                  {f.required && <span style={styles.req}> *</span>}
                </label>
                <input
                  style={inp(f.key)}
                  type={f.type}
                  placeholder={f.placeholder}
                  value={form[f.key]}
                  onChange={(e) => set(f.key, e.target.value)}
                  onFocus={() => setFocused(f.key)}
                  onBlur={() => setFocused(null)}
                />
                {errors[f.key] && <p style={styles.fieldErr}>⚠ {errors[f.key]}</p>}
              </div>
            ))}
          </div>

          {/* Третий ряд — телефон + возраст (необязательные) */}
          <div style={styles.row}>
            {fields.slice(4, 6).map((f) => (
              <div key={f.key} style={styles.field}>
                <label style={styles.label}>
                  {f.label}
                  <span style={styles.optional}> (необязательно)</span>
                </label>
                <input
                  style={inp(f.key)}
                  type={f.type}
                  placeholder={f.placeholder}
                  value={form[f.key]}
                  onChange={(e) => set(f.key, e.target.value)}
                  onFocus={() => setFocused(f.key)}
                  onBlur={() => setFocused(null)}
                />
                {errors[f.key] && <p style={styles.fieldErr}>⚠ {errors[f.key]}</p>}
              </div>
            ))}
          </div>
        </div>

        {/* Кнопка */}
        <button
          style={{ ...styles.btn, opacity: loading ? 0.7 : 1 }}
          onClick={handleRegister}
          disabled={loading}
        >
          {loading ? 'Создаём аккаунт...' : 'Создать аккаунт →'}
        </button>

        {/* Ссылка на вход */}
        <p style={styles.loginLink}>
          Уже есть аккаунт?{' '}
          <Link to='/login' style={styles.link}>Войти</Link>
        </p>
      </div>
    </div>
  )
}

const styles = {
  page: {
    minHeight: '90vh', display: 'flex',
    alignItems: 'center', justifyContent: 'center',
    padding: '40px 24px', position: 'relative', overflow: 'hidden',
  },
  blob1: {
    position: 'fixed', top: '5%', left: '10%',
    width: '600px', height: '600px', borderRadius: '50%',
    background: 'radial-gradient(circle, rgba(123,79,255,0.1), transparent 70%)',
    filter: 'blur(40px)', pointerEvents: 'none',
  },
  blob2: {
    position: 'fixed', bottom: '5%', right: '10%',
    width: '500px', height: '500px', borderRadius: '50%',
    background: 'radial-gradient(circle, rgba(59,158,255,0.08), transparent 70%)',
    filter: 'blur(40px)', pointerEvents: 'none',
  },
  card: {
    position: 'relative', width: '100%', maxWidth: '640px',
    background: 'rgba(255,255,255,0.04)',
    backdropFilter: 'blur(24px)', WebkitBackdropFilter: 'blur(24px)',
    border: '1px solid rgba(255,255,255,0.09)',
    borderRadius: '24px', padding: '40px',
    boxShadow: '0 32px 80px rgba(0,0,0,0.5)',
    overflow: 'hidden',
  },
  topLine: {
    position: 'absolute', top: 0, left: 0, right: 0, height: '2px',
    background: 'linear-gradient(90deg, #7B4FFF, #3B9EFF, #7B4FFF)',
  },
  header: {
    display: 'flex', alignItems: 'center',
    gap: '16px', marginBottom: '32px',
  },
  logoBox: {
    width: '52px', height: '52px', borderRadius: '14px', flexShrink: 0,
    background: 'linear-gradient(135deg, #7B4FFF, #3B9EFF)',
    display: 'flex', alignItems: 'center', justifyContent: 'center',
    boxShadow: '0 8px 24px rgba(123,79,255,0.4)',
  },
  logoLetter: {
    fontFamily: "'Unbounded', sans-serif",
    fontSize: '22px', fontWeight: '900', color: '#fff',
  },
  title: {
    fontFamily: "'Unbounded', sans-serif",
    fontSize: '22px', fontWeight: '700', color: '#eeeef8', margin: '0 0 4px',
  },
  subtitle: { color: '#555570', fontSize: '13px', margin: 0 },
  errorBox: {
    background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.25)',
    borderRadius: '10px', padding: '12px 16px',
    color: '#fca5a5', fontSize: '14px', marginBottom: '20px',
  },
  fields: { display: 'flex', flexDirection: 'column', gap: '16px', marginBottom: '24px' },
  row: { display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' },
  field: { display: 'flex', flexDirection: 'column', gap: '7px' },
  label: {
    fontSize: '11px', fontWeight: '600', color: '#555570',
    textTransform: 'uppercase', letterSpacing: '0.6px',
  },
  req: { color: '#a78bff' },
  optional: { color: '#333355', fontWeight: '400', textTransform: 'none', letterSpacing: 0 },
  input: {
    background: 'rgba(255,255,255,0.05)',
    border: '1px solid rgba(255,255,255,0.08)',
    borderRadius: '10px', padding: '11px 14px',
    color: '#eeeef8', fontSize: '14px', outline: 'none',
    fontFamily: "'Inter', sans-serif",
    transition: 'all 0.2s',
  },
  inputFocused: {
    background: 'rgba(123,79,255,0.08)',
    borderColor: 'rgba(123,79,255,0.45)',
    boxShadow: '0 0 0 3px rgba(123,79,255,0.08)',
  },
  inputError: {
    borderColor: 'rgba(239,68,68,0.5)',
    background: 'rgba(239,68,68,0.06)',
  },
  fieldErr: { color: '#fca5a5', fontSize: '11px', margin: 0 },
  btn: {
    width: '100%', padding: '14px',
    background: 'linear-gradient(135deg, #7B4FFF, #3B9EFF)',
    border: 'none', borderRadius: '12px',
    color: '#fff', fontSize: '15px', fontWeight: '700',
    cursor: 'pointer', fontFamily: "'Inter', sans-serif",
    boxShadow: '0 8px 28px rgba(123,79,255,0.35)',
    marginBottom: '20px',
  },
  loginLink: {
    textAlign: 'center', color: '#555570', fontSize: '14px',
  },
  link: {
    color: '#a78bff', textDecoration: 'none', fontWeight: '600',
  },
}

export default RegisterPage
