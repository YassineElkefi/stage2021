import { Component, OnInit } from '@angular/core';
import { ViewEncapsulation } from '@angular/core';
import { Router } from '@angular/router';

@Component({
  encapsulation: ViewEncapsulation.None,
  selector: 'app-auth',
  templateUrl: './auth.component.html',
  styleUrls: ['./auth.component.css']
})
export class AuthComponent implements OnInit {
  router:any; 
  bodyTag: HTMLBodyElement = document.getElementsByTagName('body')[0];
  htmlTag: HTMLElement = document.getElementsByTagName('html')[0];
  constructor(router:Router) { 
  this.router = router;
}
  ngOnInit(): void {  
  this.bodyTag.classList.add('login-page');
  this.htmlTag.classList.add('login-page');
  }
  async login(){
    var email=(<HTMLInputElement>document.getElementById("mail")).value;
    var password=(<HTMLInputElement>document.getElementById("pwd")).value;
    console.log(email)
    const response = await fetch("http://127.0.0.1:8000/login", {
      method: 'POST',
      body:`{"user":"${email}","pwd":"${password}"}`});
      if(response.ok){
          response.json().then(async (data) =>{
            console.log(data);
            if (JSON.stringify(data) !="[]"){
              if(JSON.stringify(data[0].matricule) != "1"){
                sessionStorage.id=JSON.stringify(data[0].matricule)
                console.log(data)
                this.router.navigate(['ajout-client']);
              }
              else{
                sessionStorage.id=JSON.stringify(data[0].matricule)
                console.log(data)
                this.router.navigate(['interface-admin']);
              }
              
            }
            else{
              alert("Wrong Coordinates")
              var d = document.getElementById("wrong");
              if(!d){document.getElementById("wrongholder")!.insertAdjacentHTML('beforeend', '<b style="color: red;" id = "wrong">Email/password invalid</b>');}
            }
          });
}
}
}
