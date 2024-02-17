import {useState, useEffect} from 'react'
import axios from 'axios'
import Modal from './Modal.js';
import { useParams, Link } from 'react-router-dom';
import '../css/user_profile.css'

const UserProfile = () => {
    const { id } = useParams();
    
    const [applications,setApplications] = useState([])
    const [modal,setModal] = useState(false)
    const [status_modal,setStatusModal] = useState(false)
    const [data,setData] = useState({
        application_name: '',
        credit_score: 0,
        user_id: id,
        loan_purpose :"",
        loan_amount:0,
        income :0,
        employment_status :""
      })

    const [status,setStatus] = useState({})
    const [refresh,setRefresh] = useState(false)

    useEffect(()=>{

        axios.post('http://127.0.0.1:5000/get_all_per_user',{'id':id})
        .then(data=>{
            setApplications(data.data)
        })
        .catch(e =>{
            console.log(e)
        })

    },[refresh])

    const create_new_loan = () => {

        axios.post('http://127.0.0.1:5000/create_new_loan_application',{data})
        .then(data=>{
            setRefresh(!refresh)
        })
        .catch(e =>{
            console.log(e)
        })
    
        setData({
            application_name: '',
            credit_score: 0,
            user_id: id,
            loan_purpose :"",
            loan_amount:0,
            income :0,
            employment_status :""
          })
        setModal(false)
    }

    const getStatus = (id) => {

        setStatusModal(true)

        axios.post('http://127.0.0.1:5000/get_status',{id})
        .then(data=>{
            setStatus(data.data)
        })
        .catch(e =>{
            console.log(e)
        })
        
    }

    return (
        <div className="Applications">
            <Link to={`/`}><p>Go Back</p></Link>
            <h1>Loan Applications</h1>
    
            <button onClick={()=> setModal(!modal)}>Add Application</button>

            <Modal show={status_modal} handleClose={()=> setStatusModal(false)}>
              <h1>Status</h1>
    
              <div className='add_application'>
                <label for="username">Risk Score:</label>
                <p>{status.risk_score}</p>

                <label for="score">Status:</label>
                <p>{status.status}</p>

                </div>
            </Modal>
    
            <Modal show={modal} handleClose={()=> setModal(false)}>
              <h1>Add Application</h1>
    
              <div className='add_application'>
                <label for="username">Application Name:</label>
                <input type="text" id="name" name="name" required onChange={(e)=> setData((prevObject) => ({
                                                                            ...prevObject,
                                                                            application_name: e.target.value, 
                                                                            }))}/>

                <label for="score">Credit Score:</label>
                <input type="text" id="score" name="score" required onChange={(e)=> setData((prevObject) => ({
                                                                            ...prevObject,
                                                                            credit_score: e.target.value, 
                                                                            }))}/>

                <label for="purpose">Loan Purpose:</label>
                <input type="text" id="purpose" name="purpose" required onChange={(e)=> setData((prevObject) => ({
                                                                            ...prevObject,
                                                                            loan_purpose: e.target.value, 
                                                                            }))}/>

                <label for="amount">Loan Amount:</label>
                <input type="text" id="amount" name="amount" required onChange={(e)=> setData((prevObject) => ({
                                                                            ...prevObject,
                                                                            loan_amount: e.target.value, 
                                                                            }))}/>

                <label for="Income">Income:</label>
                <input type="text" id="Income" name="Income" required onChange={(e)=> setData((prevObject) => ({
                                                                            ...prevObject,
                                                                            income: e.target.value, 
                                                                            }))}/>

                <label for="employment">Employment:</label>
                <input type="text" id="employment" name="employment" required onChange={(e)=> setData((prevObject) => ({
                                                                            ...prevObject,
                                                                            employment_status: e.target.value, 
                                                                            }))}/>
    
                <button onClick={create_new_loan} >Add</button>
              </div>
            </Modal>
    
            {applications.length ? <table>
                <thead>
                    <tr>
                        <td></td>
                        <td>Application Name</td>
                        <td>Credit Score</td>
                        <td>Loan Purpose</td>
                        <td>Loan Amount</td>
                        <td>Income</td>
                        <td>Employment Status</td>
                    </tr>
                </thead>
            
                <tbody>
                        {applications.map(val=>{
                        return (
                            <tr>
                                <td><button onClick={()=>getStatus(val.id)}>Get Status</button></td>
                                <td>{val.application_name}</td>
                                <td>{val.credit_score}</td>
                                <td>{val.loan_purpose}</td>
                                <td>{val.loan_amount}</td>
                                <td>{val.income}</td>
                                <td>{val.employment_status}</td>
                            </tr>
                        )
                        })}
                </tbody>
            </table> : null
            }
    
        </div>
      );

  };

export default UserProfile