import { useState,useEffect } from 'react'
import './App.css'

function App() {
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [status, setStatus] = useState('')
  const [lists, setLists] = useState([])

  async function deleteTodo(id){
    try{
      const response = await fetch(`http://localhost:8000/deleteTodo/${id}`,{
        method:'GET'
      })
      const result = await response.json()
      console.log(result.message)
    }catch(error){
      console.error(error)
    }


  }
  async function sendData(e) {
    e.preventDefault() // Prevent page refresh
    try {
      const response = await fetch('http://localhost:8000/addTodo', {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          title,
          description
        })
      })
      const result = await response.json()
      console.log(result)
    } catch (error) {
      console.error(error)
    }
  }

  async function getData(){
    try{
      const response = await fetch('http://localhost:8000/getTodo',{
        method:"GET"
      })

      const result = await response.json()
      setLists(result.lists)
    }catch(error){
      console.error(error)
    }
  }


  useEffect(()=>{
    getData()
  },[lists])

  return (
   <>
    <form onSubmit={sendData}>
      <input
        type="text"
        placeholder="Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />
      <input
        type="text"
        placeholder="Description"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
      />

      <button type="submit">Submit</button>
    </form>

    {lists.map(element=>{
      return(
        <div key={element.id}>
        <p>{element.title}</p>
        <p>{element.description}</p>
        <button onClick={()=>{deleteTodo(element.id)}}>Delete Todo</button>
        </div>
      )
    })}

    </>
  )
}

export default App