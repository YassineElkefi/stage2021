import { Component, OnInit } from '@angular/core';
import * as html2pdf from 'html2pdf.js';
import * as XLSX from 'xlsx';

@Component({
  selector: 'app-consultall',
  templateUrl: './consultall.component.html',
  styleUrls: ['./consultall.component.css']
})
export class ConsultallComponent implements OnInit {

  constructor() { }
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
  }
OnExportClickPDF(){
  const options= {
    filename: 'Rapport.pdf',
    html2canvas:{},
    jsPDF: {orientation: 'portrait'}
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

