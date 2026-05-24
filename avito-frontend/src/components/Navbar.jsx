import { Link, useNavigate } from 'react-router-dom'
import { useState } from 'react'

function Navbar({ onSearch }) {
  const navigate = useNavigate()
  const isLoggedIn = !!localStorage.getItem('access_token')
  const [search, setSearch] = useState('')
  const [focused, setFocused] = useState(false)

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    navigate('/login')
    window.location.reload()
  }

  const handleSearch = (e) => {
    e.preventDefault()
    if (onSearch) onSearch(search)
  }

  return (
    <nav style={styles.nav}>
      {/* Нижняя градиентная линия навбара */}
      <div style={styles.bottomLine} />

      <div style={styles.inner}>

        {/* Лого */}
        <Link to='/' style={styles.logo}>
          <div style={styles.logoGlow} />
          <div style={styles.logoBox}>
            <span style={styles.logoLetter}>А</span>
          </div>
          <span style={styles.logoText}>ВИТО</span>
        </Link>

        {/* Поиск */}
        <form onSubmit={handleSearch} style={styles.searchWrap}>
          <div style={{ ...styles.searchBox, ...(focused ? styles.searchFocused : {}) }}>
            <span style={styles.searchIcon}>⌕</span>
            <input
              style={styles.searchInput}
              type='text'
              placeholder='Найти товар...'
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              onFocus={() => setFocused(true)}
              onBlur={() => setFocused(false)}
            />
            {search && (
              <button type='submit' style={styles.searchBtn}>→</button>
            )}
          </div>
        </form>

        {/* Кнопки — одна кнопка вместо двух */}
        <div style={styles.actions}>
          {isLoggedIn ? (
            <>
              <Link to='/' style={styles.navLink}>Товары</Link>
              <Link to='/cart' style={styles.cartBtn}>
                <span>🛒</span>
                <span>Корзина</span>
              </Link>
              <button onClick={handleLogout} style={styles.outlineBtn}>
                Выйти
              </button>
            </>
          ) : (
            <>
              <Link to='/' style={styles.navLink}>Товары</Link>
              {/* Одна кнопка входа вместо двух */}
              <Link to='/login' style={styles.loginBtn}>
                <span style={styles.loginBtnInner}>Войти</span>
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  )
}

const styles = {
  nav: {
    position: 'sticky', top: 0, zIndex: 100,
    background: 'rgba(8,8,16,0.85)',
    backdropFilter: 'blur(24px)',
    WebkitBackdropFilter: 'blur(24px)',
    borderBottom: '1px solid rgba(123,79,255,0.15)',
  },
  bottomLine: {
    position: 'absolute', bottom: 0, left: 0, right: 0,
    height: '1px',
    background: 'linear-gradient(90deg, transparent, rgba(123,79,255,0.4), rgba(59,158,255,0.4), transparent)',
  },
  inner: {
    maxWidth: '1280px', margin: '0 auto',
    padding: '0 32px', height: '66px',
    display: 'flex', alignItems: 'center', gap: '20px',
    position: 'relative',
  },
  logo: {
    display: 'flex', alignItems: 'center', gap: '8px',
    textDecoration: 'none', flexShrink: 0, position: 'relative',
  },
  logoGlow: {
    position: 'absolute', left: '-8px', top: '50%',
    transform: 'translateY(-50%)',
    width: '48px', height: '48px',
    background: 'radial-gradient(circle, rgba(123,79,255,0.45), transparent 70%)',
    pointerEvents: 'none',
  },
  logoBox: {
    width: '34px', height: '34px', borderRadius: '9px',
    background: 'linear-gradient(135deg, #7B4FFF, #3B9EFF)',
    display: 'flex', alignItems: 'center', justifyContent: 'center',
    boxShadow: '0 0 16px rgba(123,79,255,0.5)',
    position: 'relative',
  },
  logoLetter: {
    fontFamily: "'Unbounded', sans-serif",
    fontWeight: '900', fontSize: '16px', color: '#fff',
  },
  logoText: {
    fontFamily: "'Unbounded', sans-serif",
    fontWeight: '800', fontSize: '16px', letterSpacing: '2px',
    background: 'linear-gradient(135deg, #c4b5fd, #93c5fd)',
    WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
    position: 'relative',
  },
  searchWrap: { flex: 1, maxWidth: '500px' },
  searchBox: {
    display: 'flex', alignItems: 'center', gap: '8px',
    background: 'rgba(255,255,255,0.05)',
    border: '1px solid rgba(255,255,255,0.08)',
    borderRadius: '12px', padding: '0 12px',
    transition: 'all 0.2s',
  },
  searchFocused: {
    background: 'rgba(123,79,255,0.08)',
    borderColor: 'rgba(123,79,255,0.4)',
    boxShadow: '0 0 0 3px rgba(123,79,255,0.08)',
  },
  searchIcon: { color: '#444466', fontSize: '20px', flexShrink: 0 },
  searchInput: {
    flex: 1, background: 'transparent !important',
    border: 'none', outline: 'none',
    color: '#eeeef8', fontSize: '14px',
    padding: '11px 0',
    fontFamily: "'Inter', sans-serif",
  },
  searchBtn: {
    background: 'linear-gradient(135deg, #7B4FFF, #3B9EFF)',
    border: 'none', borderRadius: '8px',
    padding: '5px 12px', color: '#fff',
    fontSize: '16px', cursor: 'pointer', flexShrink: 0,
  },
  actions: {
    display: 'flex', alignItems: 'center',
    gap: '10px', flexShrink: 0,
  },
  navLink: {
    color: '#7777aa', textDecoration: 'none',
    fontSize: '14px', fontWeight: '500',
    padding: '8px 12px', borderRadius: '8px',
    transition: 'color 0.2s',
  },
  cartBtn: {
    display: 'flex', alignItems: 'center', gap: '6px',
    color: '#7777aa', textDecoration: 'none',
    fontSize: '13px', fontWeight: '500',
    padding: '8px 14px', borderRadius: '10px',
    background: 'rgba(255,255,255,0.04)',
    border: '1px solid rgba(255,255,255,0.07)',
  },
  outlineBtn: {
    background: 'transparent',
    border: '1px solid rgba(255,255,255,0.1)',
    color: '#7777aa', borderRadius: '10px',
    padding: '8px 16px', fontSize: '13px',
    cursor: 'pointer', fontFamily: "'Inter', sans-serif",
    transition: 'all 0.2s',
  },
  // Одна кнопка входа с градиентом
  loginBtn: {
    textDecoration: 'none',
    background: 'linear-gradient(135deg, #7B4FFF, #3B9EFF)',
    borderRadius: '10px', padding: '1.5px',
    boxShadow: '0 4px 16px rgba(123,79,255,0.3)',
  },
  loginBtnInner: {
    display: 'block',
    background: '#080810',
    borderRadius: '9px', padding: '8px 20px',
    color: '#c4b5fd', fontSize: '14px', fontWeight: '600',
    fontFamily: "'Inter', sans-serif",
    transition: 'background 0.2s',
  },
}

export default Navbar
