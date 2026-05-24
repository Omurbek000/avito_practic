import { Routes, Route, Navigate } from 'react-router-dom'
import { useState } from 'react'
import './App.css'
import Navbar from './components/Navbar'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import ProductsPage from './pages/ProductsPage'
import ProductDetail from './pages/ProductDetail'
import CartPage from './pages/CartPage'
import AddProductPage from './pages/AddProductPage'

function App() {
  const [searchQuery, setSearchQuery] = useState('')

  return (
    <div style={{ background: '#080810', minHeight: '100vh' }}>
      <Navbar onSearch={setSearchQuery} />
      <Routes>
        <Route path='/'              element={<ProductsPage searchQuery={searchQuery} />} />
        <Route path='/login'         element={<LoginPage />} />
        <Route path='/register'      element={<RegisterPage />} />
        <Route path='/products/:id'  element={<ProductDetail />} />
        <Route path='/cart'          element={<CartPage />} />
        <Route path='/add-product'   element={<AddProductPage />} />
        <Route path='*'              element={<Navigate to='/' />} />
      </Routes>
    </div>
  )
}

export default App
