import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-ajout-client',
  templateUrl: './ajout-client.component.html',
  styleUrls: ['./ajout-client.component.css']
})
export class AjoutClientComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
  }
  async Add(){
    var cli = (<HTMLInputElement>document.getElementById("client")).value
    var adr = (<HTMLInputElement>document.getElementById("adresse")).value
    var tel = (<HTMLInputElement>document.getElementById("tel")).value
    var fax = (<HTMLInputElement>document.getElementById("fax")).value
    var mail = (<HTMLInputElement>document.getElementById("mail")).value
    var body = `{"client":"${cli}" , "adresse":"${adr}" , "tel":"${tel}" , "fax":"${fax}", "mail":"${mail}"}` 
    const rep = await fetch("http://127.0.0.1:8000/add" , {
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
