import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import api from '../api/axios'

function AddProductPage() {
  const navigate = useNavigate()
  const [form, setForm] = useState({
    product_name: '', price: '', description: '',
    product_type: 'new', sub_category: '',
  })
  const [images, setImages] = useState([])   // файлы фото
  const [previews, setPreviews] = useState([]) // превью фото
  const [subcategories, setSubcategories] = useState([])
  const [errors, setErrors] = useState({})
  const [loading, setLoading] = useState(false)
  const [focused, setFocused] = useState(null)

  // Проверяем авторизацию
  useEffect(() => {
    if (!localStorage.getItem('access_token')) {
      navigate('/login')
      return
    }
    // Загружаем подкатегории для выпадающего списка
    api.get('/subcategories/')
      .then((r) => setSubcategories(r.data.results || r.data))
      .catch(console.error)
  }, [])

  const set = (key, val) => setForm((p) => ({ ...p, [key]: val }))

  // Обработка выбора фото
  const handleImages = (e) => {
    const files = Array.from(e.target.files)
    if (files.length > 5) { alert('Максимум 5 фотографий'); return }
    setImages(files)
    // Генерируем превью
    const urls = files.map((f) => URL.createObjectURL(f))
    setPreviews(urls)
  }

  const removeImage = (idx) => {
    setImages((p) => p.filter((_, i) => i !== idx))
    setPreviews((p) => p.filter((_, i) => i !== idx))
  }

  const validate = () => {
    const e = {}
    if (!form.product_name.trim()) e.product_name = 'Введите название'
    if (!form.price || form.price <= 0) e.price = 'Введите цену'
    if (!form.sub_category) e.sub_category = 'Выберите подкатегорию'
    return e
  }

  const handleSubmit = async () => {
    const e = validate()
    if (Object.keys(e).length > 0) { setErrors(e); return }
    setErrors({}); setLoading(true)

    try {
      // Шаг 1 — создаём товар
      const productRes = await api.post('/products/', {
        product_name: form.product_name,
        price: parseInt(form.price),
        description: form.description,
        product_type: form.product_type,
        sub_category: parseInt(form.sub_category),
      })
      const productId = productRes.data.id

      // Шаг 2 — загружаем фото если есть
      if (images.length > 0) {
        for (const img of images) {
          const fd = new FormData()
          fd.append('product', productId)
          fd.append('product_image', img)
          await api.post('/product-images/', fd, {
            headers: { 'Content-Type': 'multipart/form-data' },
          })
        }
      }

      // Успех — идём на страницу товара
      navigate(`/products/${productId}`)
    } catch (err) {
      const data = err.response?.data
      if (data) {
        const mapped = {}
        Object.keys(data).forEach((key) => {
          mapped[key] = Array.isArray(data[key]) ? data[key][0] : data[key]
        })
        setErrors(mapped)
      } else {
        setErrors({ general: 'Ошибка при создании товара' })
      }
    } finally { setLoading(false) }
  }

  const inp = (f) => ({
    ...st.input,
    ...(focused === f ? st.inputFocused : {}),
    ...(errors[f] ? st.inputError : {}),
  })

  return (
    <div style={st.page}>
      <div style={st.blob1} /><div style={st.blob2} />

      <div style={st.container}>
        {/* Шапка */}
        <div style={st.header}>
          <button style={st.back} onClick={() => navigate(-1)}>← Назад</button>
          <div>
            <h1 style={st.title}>Новое объявление</h1>
            <p style={st.subtitle}>Заполните информацию о товаре</p>
          </div>
        </div>

        <div style={st.layout}>
          {/* Левая колонка — фото */}
          <div style={st.photoCard}>
            <div style={st.topLine} />
            <p style={st.sectionTitle}>Фотографии</p>
            <p style={st.sectionHint}>До 5 фото · JPG, PNG, WEBP</p>

            {/* Загрузчик */}
            <label style={st.uploadArea}>
              <input type='file' accept='image/*' multiple onChange={handleImages}
                style={{ display: 'none' }} />
              <span style={{ fontSize: '32px' }}>📸</span>
              <span style={st.uploadText}>Нажми чтобы выбрать фото</span>
              <span style={st.uploadHint}>или перетащи сюда</span>
            </label>

            {/* Превью */}
            {previews.length > 0 && (
              <div style={st.previews}>
                {previews.map((url, i) => (
                  <div key={i} style={st.previewItem}>
                    <img src={url} alt='' style={st.previewImg} />
                    <button style={st.removeImg} onClick={() => removeImage(i)}>✕</button>
                    {i === 0 && <span style={st.mainBadge}>Главное</span>}
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Правая колонка — форма */}
          <div style={st.formCard}>
            <div style={st.topLine} />

            {errors.general && <div style={st.errorBox}>⚠️ {errors.general}</div>}

            <div style={st.fields}>
              {/* Название */}
              <div style={st.field}>
                <label style={st.label}>Название <span style={st.req}>*</span></label>
                <input style={inp('product_name')} type='text'
                  placeholder='Например: iPhone 15 Pro'
                  value={form.product_name}
                  onChange={(e) => set('product_name', e.target.value)}
                  onFocus={() => setFocused('product_name')}
                  onBlur={() => setFocused(null)} />
                {errors.product_name && <p style={st.fieldErr}>⚠ {errors.product_name}</p>}
              </div>

              {/* Цена + тип */}
              <div style={st.row}>
                <div style={st.field}>
                  <label style={st.label}>Цена (сом) <span style={st.req}>*</span></label>
                  <input style={inp('price')} type='number' placeholder='10000'
                    value={form.price} onChange={(e) => set('price', e.target.value)}
                    onFocus={() => setFocused('price')} onBlur={() => setFocused(null)} />
                  {errors.price && <p style={st.fieldErr}>⚠ {errors.price}</p>}
                </div>
                <div style={st.field}>
                  <label style={st.label}>Состояние <span style={st.req}>*</span></label>
                  <select style={st.select} value={form.product_type}
                    onChange={(e) => set('product_type', e.target.value)}>
                    <option value='new'>Новый</option>
                    <option value='used'>Б/у</option>
                    <option value='reserved'>Резерв</option>
                  </select>
                </div>
              </div>

              {/* Подкатегория */}
              <div style={st.field}>
                <label style={st.label}>Подкатегория <span style={st.req}>*</span></label>
                <select style={{ ...st.select, ...(errors.sub_category ? st.inputError : {}) }}
                  value={form.sub_category}
                  onChange={(e) => set('sub_category', e.target.value)}>
                  <option value=''>— Выберите подкатегорию —</option>
                  {subcategories.map((sc) => (
                    <option key={sc.id} value={sc.id}>{sc.sub_category_name}</option>
                  ))}
                </select>
                {errors.sub_category && <p style={st.fieldErr}>⚠ {errors.sub_category}</p>}
              </div>

              {/* Описание */}
              <div style={st.field}>
                <label style={st.label}>Описание</label>
                <textarea style={st.textarea} rows={5}
                  placeholder='Опишите товар подробнее: состояние, комплектация, причина продажи...'
                  value={form.description}
                  onChange={(e) => set('description', e.target.value)} />
              </div>
            </div>

            {/* Кнопка */}
            <button
              style={{ ...st.btn, opacity: loading ? 0.7 : 1 }}
              onClick={handleSubmit} disabled={loading}
            >
              {loading ? 'Публикуем...' : '🚀 Опубликовать объявление'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

const st = {
  page: { minHeight: '90vh', padding: '0 0 60px', position: 'relative', overflow: 'hidden' },
  blob1: {
    position: 'fixed', top: '-10%', right: '5%',
    width: '500px', height: '500px', borderRadius: '50%',
    background: 'radial-gradient(circle, rgba(123,79,255,0.09), transparent 70%)',
    filter: 'blur(40px)', pointerEvents: 'none',
  },
  blob2: {
    position: 'fixed', bottom: '-10%', left: '5%',
    width: '400px', height: '400px', borderRadius: '50%',
    background: 'radial-gradient(circle, rgba(59,158,255,0.07), transparent 70%)',
    filter: 'blur(40px)', pointerEvents: 'none',
  },
  container: { maxWidth: '1100px', margin: '0 auto', padding: '32px' },
  header: { display: 'flex', alignItems: 'center', gap: '20px', marginBottom: '32px' },
  back: {
    background: 'rgba(255,255,255,0.04)', border: '1px solid rgba(255,255,255,0.08)',
    borderRadius: '10px', color: '#7777aa', padding: '10px 16px',
    cursor: 'pointer', fontFamily: "'Inter', sans-serif", fontSize: '14px',
    flexShrink: 0,
  },
  title: {
    fontFamily: "'Unbounded', sans-serif", fontSize: '22px', fontWeight: '700',
    background: 'linear-gradient(135deg, #f0f0f8, #8888aa)',
    WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', margin: '0 0 4px',
  },
  subtitle: { color: '#444466', fontSize: '13px', margin: 0 },
  layout: { display: 'grid', gridTemplateColumns: '320px 1fr', gap: '24px', alignItems: 'start' },
  // Фото
  photoCard: {
    background: 'rgba(255,255,255,0.04)', backdropFilter: 'blur(16px)',
    border: '1px solid rgba(255,255,255,0.08)', borderRadius: '20px',
    padding: '24px', position: 'relative', overflow: 'hidden',
  },
  topLine: {
    position: 'absolute', top: 0, left: 0, right: 0, height: '2px',
    background: 'linear-gradient(90deg, #7B4FFF, #3B9EFF)',
  },
  sectionTitle: { fontWeight: '600', color: '#e0e0f0', fontSize: '15px', margin: '0 0 4px' },
  sectionHint: { color: '#444466', fontSize: '12px', margin: '0 0 16px' },
  uploadArea: {
    display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '8px',
    background: 'rgba(123,79,255,0.05)', border: '2px dashed rgba(123,79,255,0.25)',
    borderRadius: '14px', padding: '28px 16px', cursor: 'pointer',
    transition: 'all 0.2s', marginBottom: '16px',
  },
  uploadText: { color: '#c4b5fd', fontSize: '14px', fontWeight: '500' },
  uploadHint: { color: '#444466', fontSize: '12px' },
  previews: { display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px' },
  previewItem: { position: 'relative', borderRadius: '10px', overflow: 'hidden' },
  previewImg: { width: '100%', height: '100px', objectFit: 'cover', display: 'block' },
  removeImg: {
    position: 'absolute', top: '4px', right: '4px',
    background: 'rgba(239,68,68,0.85)', border: 'none', borderRadius: '6px',
    color: '#fff', width: '22px', height: '22px', cursor: 'pointer',
    fontSize: '11px', display: 'flex', alignItems: 'center', justifyContent: 'center',
  },
  mainBadge: {
    position: 'absolute', bottom: '4px', left: '4px',
    background: 'rgba(123,79,255,0.85)', color: '#fff',
    fontSize: '10px', fontWeight: '600', padding: '2px 6px', borderRadius: '4px',
  },
  // Форма
  formCard: {
    background: 'rgba(255,255,255,0.04)', backdropFilter: 'blur(16px)',
    border: '1px solid rgba(255,255,255,0.08)', borderRadius: '20px',
    padding: '28px', position: 'relative', overflow: 'hidden',
  },
  errorBox: {
    background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.25)',
    borderRadius: '10px', padding: '12px 16px', color: '#fca5a5',
    fontSize: '14px', marginBottom: '20px',
  },
  fields: { display: 'flex', flexDirection: 'column', gap: '18px', marginBottom: '24px' },
  row: { display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' },
  field: { display: 'flex', flexDirection: 'column', gap: '7px' },
  label: { fontSize: '11px', fontWeight: '600', color: '#555570', textTransform: 'uppercase', letterSpacing: '0.6px' },
  req: { color: '#a78bff' },
  input: {
    background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.08)',
    borderRadius: '10px', padding: '12px 14px', color: '#eeeef8',
    fontSize: '14px', outline: 'none', fontFamily: "'Inter', sans-serif", transition: 'all 0.2s',
  },
  inputFocused: { background: 'rgba(123,79,255,0.08)', borderColor: 'rgba(123,79,255,0.45)' },
  inputError: { borderColor: 'rgba(239,68,68,0.5)' },
  select: {
    background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.08)',
    borderRadius: '10px', padding: '12px 14px', color: '#eeeef8',
    fontSize: '14px', outline: 'none', fontFamily: "'Inter', sans-serif",
    cursor: 'pointer',
  },
  textarea: {
    background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.08)',
    borderRadius: '10px', padding: '12px 14px', color: '#eeeef8',
    fontSize: '14px', outline: 'none', fontFamily: "'Inter', sans-serif",
    resize: 'vertical', transition: 'all 0.2s',
  },
  fieldErr: { color: '#fca5a5', fontSize: '11px', margin: 0 },
  btn: {
    width: '100%', padding: '15px',
    background: 'linear-gradient(135deg, #7B4FFF, #3B9EFF)',
    border: 'none', borderRadius: '12px', color: '#fff',
    fontSize: '15px', fontWeight: '700', cursor: 'pointer',
    fontFamily: "'Inter', sans-serif",
    boxShadow: '0 8px 28px rgba(123,79,255,0.35)',
  },
}

export default AddProductPage
