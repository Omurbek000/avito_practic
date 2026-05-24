import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api/axios'
import { getImageUrl } from '../utils/imageHelper'

const TYPE_LABELS = { new: 'Новый', used: 'Б/у', reserved: 'Резерв', sold: 'Продан' }
const TYPE_GRAD   = {
  new:      'linear-gradient(135deg,#22c55e,#16a34a)',
  used:     'linear-gradient(135deg,#f59e0b,#d97706)',
  reserved: 'linear-gradient(135deg,#3B9EFF,#1d4ed8)',
  sold:     'linear-gradient(135deg,#ef4444,#b91c1c)',
}

function ProductCard({ product, onClick }) {
  const [hov, setHov] = useState(false)
  return (
    <div
      style={{ ...s.card, ...(hov ? s.cardHov : {}) }}
      onClick={onClick}
      onMouseEnter={() => setHov(true)}
      onMouseLeave={() => setHov(false)}
    >
      {hov && <div style={s.cardGlow} />}
      <div style={s.imgWrap}>
        {product.product_image?.[0]?.product_image ? (
          <img src={getImageUrl(product.product_image[0].product_image)} alt={product.product_name} style={s.img} />
        ) : (
          <div style={s.noImg}><span style={{ fontSize:'36px' }}>📦</span></div>
        )}
        <span style={{ ...s.badge, background: TYPE_GRAD[product.product_type] || '#444' }}>
          {TYPE_LABELS[product.product_type] || product.product_type}
        </span>
      </div>
      <div style={s.cardBody}>
        <p style={s.cardName}>{product.product_name}</p>
        <div style={s.priceRow}>
          <span style={s.price}>{product.price?.toLocaleString()}</span>
          <span style={s.cur}>сом</span>
        </div>
        <div style={s.cardFooter}>
          {product.owner && (
            <div style={s.ownerRow}>
              <div style={s.ownerAva}>{product.owner.username[0].toUpperCase()}</div>
              <span style={s.ownerName}>{product.owner.username}</span>
            </div>
          )}
          {product.get_avg_rating > 0 && (
            <span style={s.rating}>⭐ {Number(product.get_avg_rating).toFixed(1)}</span>
          )}
        </div>
      </div>
    </div>
  )
}

function ProductsPage({ searchQuery }) {
  const navigate = useNavigate()
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)
  const [filterType, setFilterType] = useState('')
  const [sortBy, setSortBy] = useState('')
  // Пагинация
  const [nextUrl, setNextUrl] = useState(null)
  const [prevUrl, setPrevUrl] = useState(null)
  const [count, setCount] = useState(0)
  const [page, setPage] = useState(1)

  const fetchProducts = async (url = null) => {
    setLoading(true)
    try {
      let res
      if (url) {
        res = await api.get(url.replace('http://localhost:8000', ''))
      } else {
        let q = '/products/?page_size=12&'
        if (searchQuery) q += `search=${searchQuery}&`
        if (filterType)  q += `product_type=${filterType}&`
        if (sortBy)      q += `ordering=${sortBy}&`
        res = await api.get(q)
      }
      // Если ответ с пагинацией (есть results)
      if (res.data.results !== undefined) {
        setProducts(res.data.results)
        setNextUrl(res.data.next)
        setPrevUrl(res.data.previous)
        setCount(res.data.count)
      } else {
        setProducts(res.data)
        setCount(res.data.length)
      }
    } catch (e) { console.error(e) }
    finally { setLoading(false) }
  }

  useEffect(() => {
    setPage(1)
    fetchProducts()
  }, [searchQuery, filterType, sortBy])

  const handleNext = () => { if (nextUrl) { setPage(p => p+1); fetchProducts(nextUrl) } }
  const handlePrev = () => { if (prevUrl) { setPage(p => p-1); fetchProducts(prevUrl) } }

  const filters = [
    { val:'', label:'Все' }, { val:'new', label:'Новые' },
    { val:'used', label:'Б/у' }, { val:'reserved', label:'Резерв' },
  ]
  const totalPages = Math.ceil(count / 12)

  return (
    <div style={s.page}>
      {/* Заголовок */}
      <div style={s.hero}>
        <div style={s.heroInner}>
          <h1 style={s.heroTitle}>
            {searchQuery ? `🔍 "${searchQuery}"` : 'Все объявления'}
          </h1>
          <span style={s.heroCount}>{count} товаров</span>
        </div>
      </div>

      <div style={s.container}>
        {/* Тулбар */}
        <div style={s.toolbar}>
          <div style={s.filterGroup}>
            {filters.map((f) => (
              <button key={f.val}
                style={{ ...s.filterBtn, ...(filterType === f.val ? s.filterBtnOn : {}) }}
                onClick={() => { setFilterType(f.val); setPage(1) }}>
                {f.label}
              </button>
            ))}
          </div>
          <div style={{ display:'flex', gap:'10px', alignItems:'center' }}>
            <select style={s.select} value={sortBy} onChange={(e) => { setSortBy(e.target.value); setPage(1) }}>
              <option value=''>По умолчанию</option>
              <option value='price'>Сначала дешевле</option>
              <option value='-price'>Сначала дороже</option>
              <option value='-created_date'>Сначала новые</option>
            </select>
            {localStorage.getItem('access_token') && (
              <button style={s.addBtn} onClick={() => navigate('/add-product')}>
                + Добавить
              </button>
            )}
          </div>
        </div>

        {/* Сетка */}
        {loading ? (
          <div style={s.center}><div className='spinner' /></div>
        ) : products.length === 0 ? (
          <div style={s.center}>
            <p style={{ fontSize:'48px' }}>🌑</p>
            <p style={{ color:'#555570', marginTop:'12px' }}>Ничего не найдено</p>
          </div>
        ) : (
          <>
            <div style={s.grid}>
              {products.map((p) => (
                <ProductCard key={p.id} product={p} onClick={() => navigate(`/products/${p.id}`)} />
              ))}
            </div>

            {/* Пагинация */}
            {totalPages > 1 && (
              <div style={s.pagination}>
                <button
                  style={{ ...s.pageBtn, ...(prevUrl ? {} : s.pageBtnDisabled) }}
                  onClick={handlePrev} disabled={!prevUrl}
                >← Назад</button>

                <span style={s.pageInfo}>
                  {page} / {totalPages}
                </span>

                <button
                  style={{ ...s.pageBtn, ...(nextUrl ? {} : s.pageBtnDisabled) }}
                  onClick={handleNext} disabled={!nextUrl}
                >Вперёд →</button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  )
}

const s = {
  page: { minHeight: '90vh' },
  hero: { borderBottom: '1px solid rgba(255,255,255,0.05)', padding: '32px 0 24px' },
  heroInner: {
    maxWidth: '1280px', margin: '0 auto', padding: '0 32px',
    display: 'flex', alignItems: 'baseline', gap: '16px',
  },
  heroTitle: {
    fontFamily: "'Unbounded', sans-serif", fontSize: '26px', fontWeight: '700',
    background: 'linear-gradient(135deg, #f0f0f8, #8888aa)',
    WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
  },
  heroCount: { color: '#444466', fontSize: '14px' },
  container: { maxWidth: '1280px', margin: '0 auto', padding: '24px 32px' },
  toolbar: {
    display: 'flex', alignItems: 'center',
    justifyContent: 'space-between', gap: '16px',
    marginBottom: '28px', flexWrap: 'wrap',
  },
  filterGroup: { display: 'flex', gap: '8px', flexWrap: 'wrap' },
  filterBtn: {
    padding: '8px 18px', background: 'rgba(255,255,255,0.04)',
    border: '1px solid rgba(255,255,255,0.08)', borderRadius: '30px',
    color: '#7777aa', fontSize: '13px', fontWeight: '500',
    cursor: 'pointer', fontFamily: "'Inter', sans-serif",
  },
  filterBtnOn: {
    background: 'rgba(123,79,255,0.15)',
    borderColor: 'rgba(123,79,255,0.5)', color: '#c4b5fd',
  },
  select: {
    background: 'rgba(255,255,255,0.04)', border: '1px solid rgba(255,255,255,0.08)',
    borderRadius: '10px', color: '#7777aa', padding: '8px 14px',
    fontSize: '13px', outline: 'none', cursor: 'pointer',
    fontFamily: "'Inter', sans-serif",
  },
  addBtn: {
    background: 'linear-gradient(135deg, #7B4FFF, #3B9EFF)',
    border: 'none', borderRadius: '10px', color: '#fff',
    padding: '8px 18px', fontSize: '13px', fontWeight: '600',
    cursor: 'pointer', fontFamily: "'Inter', sans-serif",
    boxShadow: '0 4px 12px rgba(123,79,255,0.3)',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))',
    gap: '20px',
  },
  // Карточка
  card: {
    position: 'relative', overflow: 'hidden',
    background: 'rgba(255,255,255,0.04)',
    backdropFilter: 'blur(12px)', WebkitBackdropFilter: 'blur(12px)',
    border: '1px solid rgba(255,255,255,0.08)',
    borderRadius: '20px', cursor: 'pointer',
    transition: 'transform 0.25s, border-color 0.25s, box-shadow 0.25s',
  },
  cardHov: {
    transform: 'translateY(-6px)',
    borderColor: 'rgba(123,79,255,0.35)',
    boxShadow: '0 20px 60px rgba(123,79,255,0.15)',
  },
  cardGlow: {
    position: 'absolute', top: 0, left: 0, right: 0, height: '2px',
    background: 'linear-gradient(90deg, #7B4FFF, #3B9EFF)', zIndex: 1,
  },
  imgWrap: { position: 'relative', overflow: 'hidden' },
  img: { width: '100%', height: '190px', objectFit: 'cover', display: 'block' },
  noImg: {
    width: '100%', height: '190px', background: 'rgba(255,255,255,0.03)',
    display: 'flex', alignItems: 'center', justifyContent: 'center',
  },
  badge: {
    position: 'absolute', top: '12px', left: '12px',
    padding: '3px 10px', borderRadius: '20px',
    fontSize: '11px', fontWeight: '700', color: '#fff',
    boxShadow: '0 2px 8px rgba(0,0,0,0.3)',
  },
  cardBody: { padding: '16px' },
  cardName: {
    color: '#e0e0f0', fontSize: '15px', fontWeight: '600',
    marginBottom: '10px', lineHeight: 1.35,
    whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis',
  },
  priceRow: { display: 'flex', alignItems: 'baseline', gap: '4px', marginBottom: '12px' },
  price: {
    fontFamily: "'Unbounded', sans-serif", fontSize: '20px', fontWeight: '700',
    background: 'linear-gradient(135deg, #a78bff, #60a5fa)',
    WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
  },
  cur: { color: '#444466', fontSize: '13px' },
  cardFooter: {
    display: 'flex', alignItems: 'center', justifyContent: 'space-between',
    paddingTop: '12px', borderTop: '1px solid rgba(255,255,255,0.06)',
  },
  ownerRow: { display: 'flex', alignItems: 'center', gap: '6px' },
  ownerAva: {
    width: '22px', height: '22px', borderRadius: '50%',
    background: 'linear-gradient(135deg, #7B4FFF, #3B9EFF)',
    color: '#fff', fontSize: '11px', fontWeight: '700',
    display: 'flex', alignItems: 'center', justifyContent: 'center',
  },
  ownerName: { color: '#444466', fontSize: '12px' },
  rating: { color: '#7777aa', fontSize: '12px' },
  center: {
    display: 'flex', flexDirection: 'column',
    alignItems: 'center', justifyContent: 'center',
    padding: '80px', gap: '8px',
  },
  // Пагинация
  pagination: {
    display: 'flex', alignItems: 'center', justifyContent: 'center',
    gap: '20px', marginTop: '40px',
  },
  pageBtn: {
    background: 'rgba(255,255,255,0.05)',
    border: '1px solid rgba(255,255,255,0.1)',
    borderRadius: '10px', color: '#c4b5fd',
    padding: '10px 24px', fontSize: '14px', fontWeight: '600',
    cursor: 'pointer', fontFamily: "'Inter', sans-serif",
    transition: 'all 0.2s',
  },
  pageBtnDisabled: { opacity: 0.3, cursor: 'not-allowed' },
  pageInfo: {
    fontFamily: "'Unbounded', sans-serif", fontSize: '14px',
    color: '#7777aa',
  },
}

export default ProductsPage
