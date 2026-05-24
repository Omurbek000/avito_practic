import { useEffect, useState } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import api from '../api/axios'
import { getImageUrl } from '../utils/imageHelper'

const TYPE_LABELS = { new:'Новый', used:'Б/у', reserved:'Зарезервирован', sold:'Продан' }
const TYPE_GRAD   = {
  new:'linear-gradient(135deg,#22c55e,#16a34a)',
  used:'linear-gradient(135deg,#f59e0b,#d97706)',
  reserved:'linear-gradient(135deg,#3B9EFF,#1d4ed8)',
  sold:'linear-gradient(135deg,#ef4444,#b91c1c)',
}

function ProductDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [product, setProduct] = useState(null)
  const [loading, setLoading] = useState(true)
  const [added, setAdded] = useState(false)
  const [cartLoading, setCartLoading] = useState(false)

  useEffect(() => {
    api.get(`/products/${id}/`)
      .then((r) => setProduct(r.data))
      .catch(() => navigate('/'))
      .finally(() => setLoading(false))
  }, [id])

  const addToCart = async () => {
    if (!localStorage.getItem('access_token')) { navigate('/login'); return }
    setCartLoading(true)
    try {
      await api.post('/cart_item/', { product_id: product.id, quantity: 1 })
      setAdded(true)
    } catch (e) { if (e.response?.status === 401) navigate('/login') }
    finally { setCartLoading(false) }
  }

  if (loading) return (
    <div style={{ display:'flex', justifyContent:'center', alignItems:'center', height:'60vh' }}>
      <div className='spinner' />
    </div>
  )
  if (!product) return null

  return (
    <div style={styles.page}>
      <div style={styles.container}>
        {/* Хлебные крошки */}
        <button style={styles.back} onClick={() => navigate(-1)}>
          ← Назад к списку
        </button>

        <div style={styles.layout}>
          {/* Галерея */}
          <div style={styles.gallery}>
            {product.product_image?.length > 0 ? (
              product.product_image.map((img, i) => (
                <div key={i} style={i === 0 ? styles.mainImgWrap : styles.thumbWrap}>
                  <img
                    src={getImageUrl(img.product_image)}
                    alt={product.product_name}
                    style={i === 0 ? styles.mainImg : styles.thumbImg}
                  />
                </div>
              ))
            ) : (
              <div style={styles.noImg}>
                <span style={{ fontSize: '72px' }}>📦</span>
                <p style={{ color: '#555570', margin: '12px 0 0' }}>Нет фотографий</p>
              </div>
            )}
          </div>

          {/* Инфо */}
          <div style={styles.infoCard}>
            <div style={styles.infoTopLine} />

            {/* Бейдж */}
            <span style={{ ...styles.typeBadge, background: TYPE_GRAD[product.product_type] || '#444' }}>
              {TYPE_LABELS[product.product_type] || product.product_type}
            </span>

            {/* Название */}
            <h1 style={styles.productTitle}>{product.product_name}</h1>

            {/* Цена */}
            <div style={styles.priceBlock}>
              <span style={styles.priceNum}>{product.price?.toLocaleString()}</span>
              <span style={styles.priceCur}>сом</span>
            </div>

            {/* Рейтинг */}
            {product.get_count_people > 0 && (
              <div style={styles.ratingRow}>
                <span style={styles.stars}>{'★'.repeat(Math.round(product.get_avg_rating || 0))}</span>
                <span style={styles.ratingNum}>{Number(product.get_avg_rating || 0).toFixed(1)}</span>
                <span style={styles.ratingCount}>({product.get_count_people} отзывов)</span>
              </div>
            )}

            {/* Разделитель */}
            <div style={styles.divider} />

            {/* Описание */}
            {product.description && (
              <div style={styles.descBlock}>
                <p style={styles.sectionLabel}>Описание</p>
                <p style={styles.descText}>{product.description}</p>
              </div>
            )}

            {/* Мета */}
            {product.article_number && (
              <p style={styles.metaText}>Артикул: <strong style={{ color: '#8888aa' }}>#{product.article_number}</strong></p>
            )}

            {/* Кнопка корзины */}
            <button
              style={{ ...styles.cartBtn, ...(added ? styles.cartBtnAdded : {}) }}
              onClick={addToCart} disabled={added || cartLoading}
            >
              {added ? '✓ Добавлено в корзину' : cartLoading ? 'Добавляем...' : '🛒 Добавить в корзину'}
            </button>

            {/* Продавец */}
            {product.owner && (
              <div style={styles.sellerCard}>
                <p style={styles.sectionLabel}>Продавец</p>
                <div style={styles.sellerRow}>
                  <div style={styles.sellerAvatar}>
                    {product.owner.username[0].toUpperCase()}
                  </div>
                  <div>
                    <p style={styles.sellerName}>{product.owner.username}</p>
                    {product.owner.phone_number && (
                      <p style={styles.sellerPhone}>📞 {product.owner.phone_number}</p>
                    )}
                    {product.owner.get_user_rating > 0 && (
                      <p style={styles.sellerRating}>
                        ⭐ {Number(product.owner.get_user_rating).toFixed(1)} рейтинг
                      </p>
                    )}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

const styles = {
  page: { minHeight: '90vh', padding: '0 0 60px' },
  container: { maxWidth: '1200px', margin: '0 auto', padding: '28px 32px' },
  back: {
    background: 'none', border: 'none', cursor: 'pointer',
    color: '#8888aa', fontSize: '14px', padding: '0 0 24px',
    fontFamily: "'Inter', sans-serif",
    transition: 'color 0.2s',
  },
  layout: {
    display: 'grid',
    gridTemplateColumns: '1fr 420px',
    gap: '32px', alignItems: 'start',
  },
  gallery: { display: 'flex', flexDirection: 'column', gap: '10px' },
  mainImgWrap: {
    borderRadius: '20px', overflow: 'hidden',
    border: '1px solid rgba(255,255,255,0.08)',
  },
  thumbWrap: {
    borderRadius: '14px', overflow: 'hidden',
    border: '1px solid rgba(255,255,255,0.06)',
  },
  mainImg: { width: '100%', maxHeight: '440px', objectFit: 'cover', display: 'block' },
  thumbImg: { width: '100%', maxHeight: '200px', objectFit: 'cover', display: 'block' },
  noImg: {
    borderRadius: '20px', height: '380px',
    background: 'rgba(255,255,255,0.03)',
    border: '2px dashed rgba(255,255,255,0.08)',
    display: 'flex', flexDirection: 'column',
    alignItems: 'center', justifyContent: 'center',
  },
  infoCard: {
    position: 'relative', overflow: 'hidden',
    background: 'rgba(255,255,255,0.04)',
    backdropFilter: 'blur(20px)', WebkitBackdropFilter: 'blur(20px)',
    border: '1px solid rgba(255,255,255,0.08)',
    borderRadius: '24px', padding: '28px',
    display: 'flex', flexDirection: 'column', gap: '16px',
  },
  infoTopLine: {
    position: 'absolute', top: 0, left: 0, right: 0, height: '2px',
    background: 'linear-gradient(90deg, #7B4FFF, #3B9EFF)',
  },
  typeBadge: {
    display: 'inline-block', width: 'fit-content',
    padding: '4px 14px', borderRadius: '20px',
    fontSize: '12px', fontWeight: '700', color: '#fff',
    letterSpacing: '0.4px',
  },
  productTitle: {
    fontFamily: "'Unbounded', sans-serif",
    fontSize: '20px', fontWeight: '700',
    color: '#f0f0f8', lineHeight: 1.35, margin: 0,
  },
  priceBlock: { display: 'flex', alignItems: 'baseline', gap: '6px' },
  priceNum: {
    fontFamily: "'Unbounded', sans-serif", fontSize: '32px', fontWeight: '700',
    background: 'linear-gradient(135deg, #a78bff, #60a5fa)',
    WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
  },
  priceCur: { color: '#555570', fontSize: '16px' },
  ratingRow: { display: 'flex', alignItems: 'center', gap: '8px' },
  stars: { color: '#f59e0b', letterSpacing: '2px' },
  ratingNum: { color: '#f0f0f8', fontWeight: '600', fontSize: '14px' },
  ratingCount: { color: '#555570', fontSize: '13px' },
  divider: { height: '1px', background: 'rgba(255,255,255,0.06)' },
  sectionLabel: {
    fontSize: '11px', fontWeight: '600', color: '#555570',
    textTransform: 'uppercase', letterSpacing: '0.7px', margin: '0 0 8px',
  },
  descBlock: {},
  descText: { color: '#8888aa', fontSize: '14px', lineHeight: 1.7, margin: 0 },
  metaText: { color: '#555570', fontSize: '13px', margin: 0 },
  cartBtn: {
    width: '100%', padding: '15px',
    background: 'linear-gradient(135deg, #7B4FFF, #3B9EFF)',
    border: 'none', borderRadius: '12px',
    color: '#fff', fontSize: '15px', fontWeight: '700',
    cursor: 'pointer', fontFamily: "'Inter', sans-serif",
    boxShadow: '0 8px 24px rgba(123,79,255,0.3)',
    transition: 'all 0.2s',
  },
  cartBtnAdded: {
    background: 'linear-gradient(135deg, #22c55e, #16a34a)',
    boxShadow: '0 8px 24px rgba(34,197,94,0.3)',
  },
  sellerCard: {
    background: 'rgba(255,255,255,0.03)',
    border: '1px solid rgba(255,255,255,0.06)',
    borderRadius: '14px', padding: '16px',
  },
  sellerRow: { display: 'flex', alignItems: 'center', gap: '12px' },
  sellerAvatar: {
    width: '46px', height: '46px', borderRadius: '50%', flexShrink: 0,
    background: 'linear-gradient(135deg, #7B4FFF, #3B9EFF)',
    color: '#fff', fontSize: '18px', fontWeight: '700',
    display: 'flex', alignItems: 'center', justifyContent: 'center',
    boxShadow: '0 4px 12px rgba(123,79,255,0.3)',
  },
  sellerName: { margin: '0 0 3px', fontWeight: '600', color: '#e0e0f0', fontSize: '15px' },
  sellerPhone: { margin: '0 0 2px', color: '#8888aa', fontSize: '13px' },
  sellerRating: { margin: 0, color: '#8888aa', fontSize: '12px' },
}

export default ProductDetail
