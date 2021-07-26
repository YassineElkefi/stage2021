import { Component, OnInit } from '@angular/core'; 
import * as html2pdf from 'html2pdf.js';
import * as XLSX from 'xlsx';

@Component({
  selector: 'app-consult',
  templateUrl: './consult.component.html',
  styleUrls: ['./consult.component.css']
})
export class ConsultComponent implements OnInit {

  constructor() { 
  }
  client:any;
  region:any;
  bp:any;
  serv:any
  depot:any
  filename="rapport.xlsx"
  async ngOnInit(): Promise<void> {
    const repall = await fetch("http://127.0.0.1:8000/selectall");
    if (repall.ok){
      repall.json().then(data =>{
        this.depot = data;
        console.log(this.depot)
      })
    }

    const rep1 = await fetch("http://127.0.0.1:8000/selectc");
    if (rep1.ok){
      rep1.json().then(data =>{
        this.client = data;
        console.log(this.client)
      })
    }
    const rep2 = await fetch("http://127.0.0.1:8000/selectr");
    if (rep2.ok){
      rep2.json().then(data =>{
        this.region = data;
        console.log(this.region)

      })   
  }
    const rep4 = await fetch("http://127.0.0.1:8000/selects");
    if (rep4.ok){
      rep4.json().then(data =>{
        this.serv = data;
        console.log(this.serv)

      })   
  }
    }
     async f1() {
      var val=(<HTMLSelectElement>document.getElementById("reg")).value
      const rep3 = await fetch(`http://127.0.0.1:8000/selectbp?id= ${val}`);
      if (rep3.ok){
        rep3.json().then(data =>{
          this.bp = data;
          console.log(this.bp)
        })
      }
    }
    async Filtrer(){
      var cli =(<HTMLSelectElement>document.getElementById("cli")).value;
      var bp =(<HTMLSelectElement>document.getElementById("bp")).value;
      var serv=(<HTMLSelectElement>document.getElementById("service")).value;
      var date_s=(<HTMLSelectElement>document.getElementById("date_s")).value;
      var date_e=(<HTMLSelectElement>document.getElementById("date_e")).value;
    const rep = await fetch(`http://127.0.0.1:8000/selectdepot?Client=${cli}&bp=${bp}&service=${serv}&date_s=${date_s}&date_e=${date_e}`)
    rep.json().then(data =>{
    this.depot=data;
    console.log(data)
    })
}
OnExportClickPDF(){
  const options= {
    filename: 'Rapport.pdf',
    html2canvas:{},
    jsPDF: {orientation: 'landscape'}
  };
  const content: Element = document.getElementById('exp');

  html2pdf().from(content).set(options).save()
}
OnExportClickXLS():void{
let element = document.getElementById('t1');
const ws : XLSX.WorkSheet = XLSX.utils.table_to_sheet(element);

const wb : XLSX.WorkBook = XLSX.utils.book_new();

XLSX.utils.book_append_sheet(wb,ws,"sheet 1");

XLSX.writeFile(wb,this.filename);
}
}
