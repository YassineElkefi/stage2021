import { Component, OnInit } from '@angular/core';
import { disableDebugTools } from '@angular/platform-browser';
import { promise } from 'protractor';
declare const test:any;
declare const f:any;
@Component({
  selector: 'app-suppr-client',
  templateUrl: './suppr-client.component.html',
  styleUrls: ['./suppr-client.component.css']
})
export class SupprClientComponent implements OnInit {
  constructor() { }
  client:any

  async ngOnInit(): Promise<void> {

    const rep1 = await fetch("http://127.0.0.1:8000/selectc");
    if (rep1.ok){
      rep1.json().then(data =>{
        this.client = data;
        console.log(this.client)
      })
    }
}
onClick(){
  test();
}
f2(){
  f();
}
f3(){
  var modal = document.getElementById("myModal");
  modal.style.display = "none";
}

async Suppr(){
  var cl = (<HTMLSelectElement>document.getElementById("cli")).value
  var body = `{"client":"${cl}"}` 
  const rep = await fetch("http://127.0.0.1:8000/delcli" , {
    method:"delete" , 
    body : body
  })
  if (rep.ok){
    rep.json().then((data)=>{
      console.log(data)
    })
  }
  this.f3()
}
}