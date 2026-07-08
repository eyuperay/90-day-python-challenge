import React, { useState, useEffect } from 'react';
import { customerAPI } from '../api/customers';
import { useNavigate } from 'react-router-dom';

const Customers = () => {
  const [customers, setCustomers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [newCustomer, setNewCustomer] = useState({
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    company: '',
  });
  const navigate = useNavigate();

  useEffect(() => {
    loadCustomers();
  }, []);

  const loadCustomers = async () => {
    try {
      const response = await customerAPI.getAll();
      setCustomers(response.data);
    } catch (error) {
      console.error('Hata:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddCustomer = async (e) => {
    e.preventDefault();
    try {
      await customerAPI.create(newCustomer);
      setShowForm(false);
      setNewCustomer({ first_name: '', last_name: '', email: '', phone: '', company: '' });
      loadCustomers();
    } catch (error) {
      console.error('Müşteri eklenirken hata:', error);
    }
  };

  const handleDeleteCustomer = async (id) => {
    if (window.confirm('Bu müşteriyi silmek istediğinize emin misiniz?')) {
      try {
        await customerAPI.delete(id);
        loadCustomers();
      } catch (error) {
        console.error('Müşteri silinirken hata:', error);
      }
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  if (loading) return <div style={{ textAlign: 'center', marginTop: '50px' }}>Yükleniyor...</div>;

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h1>Müşteriler</h1>
        <div>
          <button onClick={() => setShowForm(!showForm)} style={styles.addButton}>
            {showForm ? '✖ Kapat' : '➕ Yeni Müşteri'}
          </button>
          <button onClick={handleLogout} style={styles.logoutButton}>
            Çıkış
          </button>
        </div>
      </div>

      {showForm && (
        <form onSubmit={handleAddCustomer} style={styles.form}>
          <h3>Yeni Müşteri Ekle</h3>
          <div style={styles.formRow}>
            <input
              style={styles.input}
              placeholder="Ad *"
              value={newCustomer.first_name}
              onChange={(e) => setNewCustomer({...newCustomer, first_name: e.target.value})}
              required
            />
            <input
              style={styles.input}
              placeholder="Soyad *"
              value={newCustomer.last_name}
              onChange={(e) => setNewCustomer({...newCustomer, last_name: e.target.value})}
              required
            />
            <input
              style={styles.input}
              placeholder="Email *"
              type="email"
              value={newCustomer.email}
              onChange={(e) => setNewCustomer({...newCustomer, email: e.target.value})}
              required
            />
            <input
              style={styles.input}
              placeholder="Telefon"
              value={newCustomer.phone}
              onChange={(e) => setNewCustomer({...newCustomer, phone: e.target.value})}
            />
            <input
              style={styles.input}
              placeholder="Şirket"
              value={newCustomer.company}
              onChange={(e) => setNewCustomer({...newCustomer, company: e.target.value})}
            />
          </div>
          <button type="submit" style={styles.submitButton}>Müşteri Ekle</button>
        </form>
      )}

      <table style={styles.table}>
        <thead>
          <tr style={styles.tableHeader}>
            <th style={styles.th}>ID</th>
            <th style={styles.th}>Ad</th>
            <th style={styles.th}>Soyad</th>
            <th style={styles.th}>Email</th>
            <th style={styles.th}>Şirket</th>
            <th style={styles.th}>İşlemler</th>
          </tr>
        </thead>
        <tbody>
          {customers.length === 0 ? (
            <tr>
              <td colSpan="6" style={styles.emptyMessage}>Henüz müşteri yok</td>
            </tr>
          ) : (
            customers.map((customer) => (
              <tr key={customer.id}>
                <td style={styles.td}>{customer.id}</td>
                <td style={styles.td}>{customer.first_name}</td>
                <td style={styles.td}>{customer.last_name}</td>
                <td style={styles.td}>{customer.email}</td>
                <td style={styles.td}>{customer.company || '-'}</td>
                <td style={styles.td}>
                  <button 
                    onClick={() => handleDeleteCustomer(customer.id)} 
                    style={styles.deleteButton}
                  >
                    🗑️ Sil
                  </button>
                </td>
              </tr>
            ))
          )}
        </tbody>
      </table>
    </div>
  );
};

const styles = {
  container: {
    padding: '20px',
    maxWidth: '1200px',
    margin: '0 auto',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '20px',
  },
  addButton: {
    padding: '10px 20px',
    backgroundColor: '#28a745',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    marginRight: '10px',
  },
  logoutButton: {
    padding: '10px 20px',
    backgroundColor: '#dc3545',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
  },
  deleteButton: {
    padding: '5px 10px',
    backgroundColor: '#dc3545',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
    fontSize: '12px',
  },
  form: {
    backgroundColor: '#f8f9fa',
    padding: '20px',
    borderRadius: '8px',
    marginBottom: '20px',
    border: '1px solid #ddd',
  },
  formRow: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: '10px',
    marginBottom: '10px',
  },
  input: {
    padding: '10px',
    border: '1px solid #ddd',
    borderRadius: '4px',
    fontSize: '14px',
  },
  submitButton: {
    padding: '10px 20px',
    backgroundColor: '#007bff',
    color: 'white',
    border: 'none',
    borderRadius: '4px',
    cursor: 'pointer',
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse',
    backgroundColor: 'white',
    borderRadius: '8px',
    overflow: 'hidden',
    boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
  },
  tableHeader: {
    backgroundColor: '#f8f9fa',
  },
  th: {
    padding: '12px',
    border: '1px solid #ddd',
    textAlign: 'left',
    fontWeight: '600',
  },
  td: {
    padding: '12px',
    border: '1px solid #ddd',
  },
  emptyMessage: {
    textAlign: 'center',
    padding: '40px',
    color: '#888',
  },
};

export default Customers;