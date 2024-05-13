document.addEventListener('DOMContentLoaded', function(){

    document.querySelector('#myDropdown').style.display = 'none';
    document.querySelector('#detail').style.display = 'none';
    document.querySelector('#monthdetail').style.display = 'none';

    document.querySelector('#myDropdownButton').addEventListener('click', function() {
        toggleDropdown('myDropdown');
    });
    document.querySelector('#detailbutton').addEventListener('click', function() {
        toggleDropdown('detail');
        calcTax();
    });
    document.querySelector('#monthdetailbutton').addEventListener('click', function() {
        var { tax: tax, socialfundTotal: socialfundTotal } = calcTax();

        toggleDropdown('monthdetail');
        calcMonth(tax, socialfundTotal);
    });

    document.querySelector('#annualincomebutton').addEventListener('click', function() {
        var { tax: tax, annualIncome: annualIncome } = calcTax();

        toggleDropdown('detail');
        calcAnnual(tax, annualIncome);
    });
    
    function toggleDropdown(elementId) {
        var element = document.getElementById(elementId);
        if (element.style.display === "none") {
            element.style.display = "block";
        } else {
            element.style.display = "none"; 
        }
    }

    function getPercent(remain) {
        if (remain <= 36000) {
            return [0, 0.03];
        } else if (remain > 36000 && remain <= 144000) {
            return [2520, 0.1];
        } else if (remain > 144000 && remain <= 300000) {
            return [16920, 0.2];
        } else if (remain > 300000 && remain <= 420000) {
            return [31920, 0.25];
        } else if (remain > 420000 && remain <= 660000) {
            return [52920, 0.3];
        } else if (remain > 660000 && remain <= 960000) {
            return [85920, 0.35];
        } else if (remain > 960000) {
            return [181920, 0.45];
        }
    }

    function getPercentAnnual(bonus){

        let remain = bonus/12

        if (remain <= 3000) {
            return [0, 0.03];
        } else if (remain > 3000 && remain <= 12000) {
            return [210, 0.1];
        } else if (remain > 12000 && remain <= 25000) {
            return [1410, 0.2];
        } else if (remain > 25000 && remain <= 35000) {
            return [2660, 0.25];
        } else if (remain > 35000 && remain <= 55000) {
            return [4410, 0.3];
        } else if (remain > 55000 && remain <= 80000) {
            return [7160, 0.35];
        } else if (remain > 80000) {
            return [15160, 0.45];
        }


    }


    function sumArray(array) {
        var total = 0;
        array.forEach(function (tax) {
            total += tax;
        });
        return total;
    }


    function calcTax() {

        var salary = parseInt(document.getElementById('salary').value);
        var base = 5000;
        var deductionElement = document.getElementById('deduction');
        
        var deductionValue = deductionElement && deductionElement.value.trim() !== '' ? parseInt(deductionElement.value) : 0;

        var social  = [7310, 36549];
        var housingfund = [2590, 36549];

        var socialfortax = salary;

        if (salary < social[0]) {
            socialfortax = social[0];
        } else if (salary > social[1]) {
            socialfortax = social[1]
        }

        var housingfundfortax = salary;

        if (salary < housingfund[0]) {
            housingfundfortax = housingfund[0];
        } else if (salary > housingfund[1]) {
            housingfundfortax = housingfund[1]
        }

        

        $('#ylgr').text((socialfortax * 0.08).toFixed(2));
        $('#ybgr').text((socialfortax * 0.02).toFixed(2));
        $('#sygr').text((socialfortax * 0.005).toFixed(2));
        $('#gjjgr').text((housingfundfortax * 0.07).toFixed(2));
    
        var socialTaxList = [socialfortax * 0.08, socialfortax * 0.02, socialfortax * 0.005];
        var socialTax= sumArray(socialTaxList);

        var housingfundTax = housingfundfortax * 0.07;


        var socialHousingfund = socialTax + housingfundTax;

        var tax = [];
        var currentDate = new Date();
        var currentMonth = currentDate.getMonth() + 1;
        var bonus = parseInt(document.getElementById('bonusinput').value);
        var annualIncome = parseFloat(salary) * 12 + parseFloat(bonus) - (parseFloat(socialHousingfund) + parseFloat(deductionValue) + parseFloat(base)) * 12;

        var taxListString = '';
        for (var i = 1; i <= 12; i++) {
            var currentMonthRemain = (salary - (socialHousingfund + deductionValue + base)) * i;
            var taxPercentInfo = getPercent(currentMonthRemain);
            tax[i] = currentMonthRemain * taxPercentInfo[1] - taxPercentInfo[0] - sumArray(tax);
            
            if (i === currentMonth) {
                var taxAmount = Math.max(tax[i], 0).toFixed(2);
                taxListString = taxAmount;
            }
        }
        document.getElementById("tax").innerHTML = taxListString;

        var socialTotal = (socialfortax * (0.08 + 0.02 + 0.005)).toFixed(2);
        var housingfund = (housingfundfortax * 0.07).toFixed(2);
        var socialfundTotal = parseFloat(socialTotal) + parseFloat(housingfund)
        
        var personTotal = (parseFloat(socialTotal) + parseFloat(housingfund) + parseFloat(taxListString)).toFixed(2);
        $('#total').text(personTotal);

        var afterTaxIncome = (parseFloat(salary) - parseFloat(personTotal)).toFixed(2);
        $('#aftertax').text(afterTaxIncome);

        return { tax: tax, socialfundTotal: socialfundTotal, annualIncome: annualIncome };
    }

    function calcMonth(tax, socialfundTotal){

        var salary = parseInt(document.getElementById('salary').value);

        for (var i = 1; i <= 12; i++) {
            var monthlyIncome = parseFloat(salary) - parseFloat(socialfundTotal) - parseFloat(tax[i]);

        document.getElementById('monthincome' + i).textContent = monthlyIncome.toFixed(2);
        document.getElementById('monthtax' + i).textContent = tax[i].toFixed(2);

        }
    }

    function calcAnnual(tax, annualIncome) {
        let salary = parseFloat(document.getElementById('salary').value).toFixed(2);
        let bonus = parseFloat(document.getElementById('bonusinput').value).toFixed(2);
 
        let bonusTaxPercent = getPercentAnnual(bonus);
        let bonusTax = (bonus * bonusTaxPercent[1] - bonusTaxPercent[0]).toFixed(2);
    
        let annualTaxPercent = getPercent(annualIncome);
        let annualTax = (annualIncome * annualTaxPercent[1] - annualTaxPercent[0]).toFixed(2);
    
        let totalTax = tax.reduce((acc, curr) => acc + curr, 0);
        let totalTaxWithBonus = (parseFloat(bonusTax) + totalTax).toFixed(2);
    
        let annualTaxResult = (totalTaxWithBonus > annualTax) ? annualTax : totalTaxWithBonus;

        let housingfundToal = (salary * 0.07 * 12).toFixed(2);
        let socialTotal = ((salary * (0.08 + 0.02 + 0.005)) * 12).toFixed(2);
    
        let annualNetSalary = (salary * 12 - annualTaxResult - parseFloat(socialTotal) - parseFloat(housingfundToal)).toFixed(2);
        let annualNetIncome = (parseFloat(annualNetSalary) + parseFloat(housingfundToal)).toFixed(2);
        
        
        const tableAnnual = document.querySelector('#detail');
        tableAnnual.innerHTML = '';

        tableAnnual.innerHTML = `
        <table class="table w-25 mx-auto table-striped border border-2 border-light">
            <thead class="table-info">
              <tr>
                <th scope="col">五险一金</th>
                <th scope="col">个人</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <th scope="row">全年社保</th>
                <td id="ylgr">${socialTotal}</td>
              </tr>
              <tr>
                <th scope="row">全年住房公积金</th>
                <td id="gjjgr">${housingfundToal}</</td>
              </tr>
              <tr>
                <th scope="row">全年缴税</th>
                <td id="tax">${annualTaxResult}</td>
              </tr>
              <tr>
                <th scope="row">税后年薪资</th>
                <td id="total">${annualNetSalary}</td>
              </tr>
              <tr class="table-dark">
                <th scope="row">税后年收入</th>
                <td id="aftertax">${annualNetIncome}</td>
              </tr>
            </tbody>
          </table>
        `;
    }
    

});
