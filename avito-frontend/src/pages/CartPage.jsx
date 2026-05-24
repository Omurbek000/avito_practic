import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api/axios'

function CartPage() {
  const navigate = useNavigate()
  const [cart, setCart] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!localStorage.getItem('access_token')) { navigate('/login'); return }
    api.get('/cart/')
      .then((r) => setCart(r.data))
      .catch(() => navigate('/login'))
      .finally(() => setLoading(false))
  }, [])

  const handleRemove = async (itemId) => {
    try {
      await api.delete(`/cart_item/${itemId}/`)
      const res = await api.get('/cart/')
      setCart(res.data)
    } catch (e) { console.error(e) }
  }

  if (loading) return (
    <div style={{ display:'flex', justifyContent:'center', alignItems:'center', height:'60vh' }}>
      <div className='spinner' />
    </div>
  )

  const items = cart?.cart_item || []

  return (
    <div style={styles.page}>
      <div style={styles.container}>
        <h1 style={styles.title}>Корзина</h1>

        {items.length === 0 ? (
          <div style={styles.empty}>
            <div style={styles.emptyTopLine} />
            <span style={{ fontSize: '52px' }}>🛒</span>
            <p style={styles.emptyText}>Корзина пуста</p>
            <button style={styles.shopBtn} onClick={() => navigate('/')}>
              Перейти к товарам →
            </button>
          </div>
        ) : (
          <div style={styles.layout}>
            {/* Список */}
            <div style={styles.itemsList}>
              {items.map((item) => (
                <div key={item.id} style={styles.item}>
                  <div style={styles.itemTopLine} />
                  <div style={styles.itemInner}>
                    <div style={styles.itemIcon}>📦</div>
                    <div style={styles.itemInfo}>
                      <p style={styles.itemName}>{item.product?.product_name}</p>
                      <p style={styles.itemQty}>Количество: {item.quantity}</p>
                    </div>
                    <div style={styles.itemRight}>
                      <div>
                        <p style={styles.itemPrice}>{item.total_price?.toLocaleString()}</p>
                        <p style={styles.itemCur}>сом</p>
                      </div>
                      <button style={styles.removeBtn} onClick={() => handleRemove(item.id)}>✕</button>
                    </div>
                  </div>
                </div>
              ))}
            </div>

            {/* Итог */}
            <div style={styles.summary}>
              <div style={styles.summaryTopLine} />
              <p style={styles.summaryTitle}>Итого</p>
              <div style={styles.summaryRow}>
                <span style={styles.summaryLabel}>Товаров</span>
                <span style={styles.summaryVal}>{items.length} шт.</span>
              </div>
              <div style={styles.summaryDivider} />
              <div style={styles.summaryRow}>
                <span style={styles.summaryLabel}>Сумма</span>
                <div>
                  <span style={styles.totalPrice}>{cart?.total_price?.toLocaleString()}</span>
                  <span style={{ color: '#555570', fontSize: '13px' }}> сом</span>
                </div>
              </div>
              <button style={styles.orderBtn}>Оформить заказ →</button>
              <button style={styles.contBtn} onClick={() => navigate('/')}>
                Продолжить покупки
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

const glass = {
  background: 'rgba(255,255,255,0.04)',
  backdropFilter: 'blur(16px)', WebkitBackdropFilter: 'blur(16px)',
  border: '1px solid rgba(255,255,255,0.08)',
}
const topLine = {
  position: 'absolute', top: 0, left: 0, right: 0, height: '2px',
  background: 'linear-gradient(90deg, #7B4FFF, #3B9EFF)',
}

const styles = {
  page: { minHeight: '90vh', padding: '0 0 60px' },
  container: { maxWidth: '1000px', margin: '0 auto', padding: '32px 32px' },
  title: {
    fontFamily: "'Unbounded', sans-serif", fontSize: '26px', fontWeight: '700',
    background: 'linear-gradient(135deg, #f0f0f8, #8888aa)',
    WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
    marginBottom: '28px',
  },
  empty: {
    ...glass, borderRadius: '24px', padding: '60px',
    textAlign: 'center', display: 'flex', flexDirection: 'column',
    alignItems: 'center', gap: '16px', position: 'relative', overflow: 'hidden',
  },
  emptyTopLine: topLine,
  emptyText: { color: '#555570', fontSize: '16px' },
  shopBtn: {
    background: 'linear-gradient(135deg, #7B4FFF, #3B9EFF)',
    color: '#fff', border: 'none', borderRadius: '12px',
    padding: '12px 28px', fontSize: '15px', fontWeight: '600',
    cursor: 'pointer', fontFamily: "'Inter', sans-serif",
    boxShadow: '0 8px 24px rgba(123,79,255,0.3)',
  },
  layout: { display: 'grid', gridTemplateColumns: '1fr 300px', gap: '24px', alignItems: 'start' },
  itemsList: { display: 'flex', flexDirection: 'column', gap: '12px' },
  item: {
    ...glass, borderRadius: '16px', padding: '20px',
    position: 'relative', overflow: 'hidden',
  },
  itemTopLine: topLine,
  itemInner: { display: 'flex', alignItems: 'center', gap: '16px' },
  itemIcon: {
    width: '52px', height: '52px', borderRadius: '12px',
    background: 'rgba(123,79,255,0.1)', border: '1px solid rgba(123,79,255,0.2)',
    display: 'flex', alignItems: 'center', justifyContent: 'center',
    fontSize: '22px', flexShrink: 0,
  },
  itemInfo: { flex: 1 },
  itemName: { margin: '0 0 4px', fontWeight: '600', color: '#e0e0f0', fontSize: '15px' },
  itemQty: { margin: 0, color: '#555570', fontSize: '13px' },
  itemRight: { display: 'flex', alignItems: 'center', gap: '16px', flexShrink: 0 },
  itemPrice: {
    margin: 0, fontFamily: "'Unbounded', sans-serif", fontWeight: '700',
    fontSize: '17px',
    background: 'linear-gradient(135deg, #a78bff, #60a5fa)',
    WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
  },
  itemCur: { margin: 0, color: '#555570', fontSize: '11px' },
  removeBtn: {
    background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.2)',
    borderRadius: '8px', padding: '7px 10px', color: '#fca5a5',
    cursor: 'pointer', fontSize: '13px', flexShrink: 0,
  },
  summary: {
    ...glass, borderRadius: '20px', padding: '24px',
    position: 'relative', overflow: 'hidden',
    display: 'flex', flexDirection: 'column', gap: '14px',
  },
  summaryTopLine: topLine,
  summaryTitle: {
    fontFamily: "'Unbounded', sans-serif", fontSize: '16px', fontWeight: '700',
    color: '#f0f0f8', margin: 0,
  },
  summaryRow: { display: 'flex', justifyContent: 'space-between', alignItems: 'baseline' },
  summaryLabel: { color: '#555570', fontSize: '14px' },
  summaryVal: { color: '#8888aa', fontSize: '14px' },
  summaryDivider: { height: '1px', background: 'rgba(255,255,255,0.06)' },
  totalPrice: {
    fontFamily: "'Unbounded', sans-serif", fontSize: '22px', fontWeight: '700',
    background: 'linear-gradient(135deg, #a78bff, #60a5fa)',
    WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
  },
  orderBtn: {
    width: '100%', padding: '14px',
    background: 'linear-gradient(135deg, #7B4FFF, #3B9EFF)',
    border: 'none', borderRadius: '12px', color: '#fff',
    fontSize: '15px', fontWeight: '700', cursor: 'pointer',
    fontFamily: "'Inter', sans-serif",
    boxShadow: '0 8px 24px rgba(123,79,255,0.3)',
  },
  contBtn: {
    width: '100%', padding: '12px',
    background: 'transparent',
    border: '1px solid rgba(255,255,255,0.08)',
    borderRadius: '12px', color: '#8888aa',
    fontSize: '14px', cursor: 'pointer',
    fontFamily: "'Inter', sans-serif",
  },
}

export default CartPage
