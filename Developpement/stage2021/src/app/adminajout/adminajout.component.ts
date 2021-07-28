import { Component, OnInit } from '@angular/core';
declare const testadd:any
@Component({
  selector: 'app-adminajout',
  templateUrl: './adminajout.component.html',
  styleUrls: ['./adminajout.component.css']
})
export class AdminajoutComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
  }
  async add(){
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
  onClick(){
    if (testadd() == true){
      this.add()
    }
  }
}
