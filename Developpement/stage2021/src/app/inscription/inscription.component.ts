import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-inscription',
  templateUrl: './inscription.component.html',
  styleUrls: ['./inscription.component.css']
})
export class InscriptionComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
  }
  async Add(){
    var n = (<HTMLInputElement>document.getElementById("nom")).value
    var p = (<HTMLInputElement>document.getElementById("prenom")).value
    var m = (<HTMLInputElement>document.getElementById("mail")).value
    var t = (<HTMLInputElement>document.getElementById("tel")).value
    var pw = (<HTMLInputElement>document.getElementById("pwd")).value
    var body = `{"nom":"${n}" , "prenom":"${p}" , "mail":"${m}" , "tel":"${t}", "pwd":"${pw}"}` 
    const rep = await fetch("http://127.0.0.1:8000/signup" , {
      method:"POST" , 
      body : body
    })
    if (rep.ok){
      rep.json().then((data)=>{
        console.log(data)
      })
    }

  }

}
