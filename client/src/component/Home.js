import {useState, useEffect} from 'react'
import axios from 'axios'
import Modal from './Modal.js';
import { Link } from 'react-router-dom';

function Home() {

  const [users,setUsers] = useState([])
  const [modal,setModal] = useState(false)
  const [name,setName] = useState('')
  const [refresh,setRefresh] = useState(false)

  useEffect(()=>{

    axios.get('http://127.0.0.1:5000/all_users')
    .then(data=>{
      setUsers(data.data)
    })
    .catch(e =>{
      console.log(e)
    })

  },[refresh])

  const create_new_user = () => {

    if(name.length){

      axios.post('http://127.0.0.1:5000/create_new_user',{'name': name})
      .then(data=>{
        setRefresh(!refresh)
      })
      .catch(e =>{
        console.log(e)
      })

      setName('')
      setModal(false)
    }

  }

  return (
    <div className="Home">
        <h1>Loan Application</h1>

        <button onClick={()=> setModal(!modal)}>Add User</button>

        <Modal show={modal} handleClose={()=> setModal(false)}>
          <h1>Add User</h1>

          <div>
            <label for="username">Username:</label>
            <input type="text" id="name" name="name" required onChange={(e)=> setName(e.target.value)}/>

            <button onClick={create_new_user} >Add</button>
          </div>
        </Modal>

        {users && users.map(val=>{
         return <Link to={`/user/${val.id}`}><p>{val.name}</p></Link>
        })}

    </div>
  );
}

export default Home;
