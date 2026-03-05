import {useState} from "react"

function RegistrationForm(){

const [name,setName] = useState("")
const [aadhaar,setAadhaar] = useState("")

const submit = async () => {

await fetch("http://localhost:8000/register",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({name,aadhaar})
})

}

return(
<div>
<h3>Register</h3>

<input
placeholder="Name"
onChange={(e)=>setName(e.target.value)}
/>

<input
placeholder="Aadhaar"
onChange={(e)=>setAadhaar(e.target.value)}
/>

<button onClick={submit}>Submit</button>

</div>
)
}

export default RegistrationForm
