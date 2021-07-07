import { Component, OnInit } from '@angular/core';
declare const test:any;
declare const f:any;
@Component({
  selector: 'app-suppr-client',
  templateUrl: './suppr-client.component.html',
  styleUrls: ['./suppr-client.component.css']
})
export class SupprClientComponent implements OnInit {
  constructor() { }

  ngOnInit(): void {
  }
  onClick(){
    test();
  }
  f2(){
    f();
  }
}
