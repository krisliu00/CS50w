
document.addEventListener('DOMContentLoaded', function(){

const originalHtml = document.querySelector('#detail').cloneNode(true);
document.querySelector('#myDropdown').style.display = 'none';
document.querySelector('#detail').style.display = 'none';
document.querySelector('#monthdetail').style.display = 'none';
document.querySelector('#input_area').style.display = 'block';

document.querySelector('#myDropdownButton').addEventListener('click', function() {
    toggleDropdown('myDropdown');
});

document.querySelector('#detailbutton').addEventListener('click', async function() {
    var { customBaseHousing, customBaseSocial, housingPercentNormal } = await socialHousingFundValue();
    toggleDropdown('detail');
    calcTax(housingPercentNormal, customBaseHousing, customBaseSocial);
});

document.querySelector('#monthdetailbutton').addEventListener('click', async function() {
    var { customBaseHousing, customBaseSocial, housingPercentNormal } = await socialHousingFundValue();
    var { tax, socialfundTotal } = await calcTax(housingPercentNormal, customBaseHousing, customBaseSocial);
    toggleDropdown('monthdetail');
    calcMonth(tax, socialfundTotal);
});

document.querySelector('#annualincomebutton').addEventListener('click', async function() {
    var { customBaseHousing, customBaseSocial, housingPercentNormal } = await socialHousingFundValue();
    var { tax, annualIncome} = await calcTax(housingPercentNormal, customBaseHousing, customBaseSocial);

    toggleDropdown('detail');
    calcAnnual(tax, annualIncome, customBaseHousing, customBaseSocial, housingPercentNormal);
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

async function socialHousingFundValue(){
    var salary = parseInt(document.getElementById('salary').value);
    var socialBaseInput = document.getElementById('customsocial');
    var housingBaseInput = document.getElementById('customhousing');
    var housingPercentInput = document.getElementById('housingpercent');
    var socialBase = socialBaseInput.value !== '' ? parseInt(socialBaseInput.value) : null;
    var housingBase = housingBaseInput.value !== '' ? parseInt(housingBaseInput.value) : null;
    var housingPercent = housingPercentInput.value !== '' ? parseFloat(housingPercentInput.value) : null;

    var socialRange = [7310, 36549];
    var housingFundRange = [2590, 36549];
    var housingPercentNormal = 0.07; 

    if (socialBase !== null) {
        socialBase = Math.min(Math.max(socialBase, socialRange[0]), socialRange[1]);
    }
    if (housingBase !== null) {
        housingBase = Math.min(Math.max(housingBase, housingFundRange[0]), housingFundRange[1]);
    }
    if (housingPercent !== null && housingPercent >= 5 && housingPercent <= 12) {
        housingPercentNormal = housingPercent / 100;
    } else if (housingPercentInput.value !== '') {
        alert("公积金基数在5%-12%之间。");
        return;
    }

    
    var customBaseHousing = housingBase !== null ? housingBase : salary;
    var customBaseSocial = socialBase !== null ? socialBase : salary;
    
    return { customBaseHousing, customBaseSocial, housingPercentNormal };

}


async function calcTax(housingPercentNormal, customBaseHousing, customBaseSocial) {
    resetToOriginalHtml();
    var salary = parseInt(document.getElementById('salary').value);
    var base = 5000;
    var deductionElement = document.getElementById('deduction');
    
    var deductionValue = deductionElement && deductionElement.value.trim() !== '' ? parseInt(deductionElement.value) : 0;

    $('#ylgr').text((customBaseSocial * 0.08).toFixed(2));
    $('#ybgr').text((customBaseSocial * 0.02).toFixed(2));
    $('#sygr').text((customBaseSocial * 0.005).toFixed(2));
    $('#gjjgr').text((customBaseHousing * housingPercentNormal).toFixed(2));

    var social = [customBaseSocial * 0.08, customBaseSocial * 0.02, customBaseSocial * 0.005];
    var socialTax= sumArray(social);

    var housingfundTax = customBaseHousing * housingPercentNormal;

    var socialHousingfund = socialTax + housingfundTax;

    var tax = new Array(12).fill(0);
    var currentDate = new Date();
    var currentMonth = currentDate.getMonth() + 1;
    var bonusValue = document.getElementById('bonusinput');
    var bonus = bonusValue && bonusValue.value.trim() !== '' ? parseInt(bonusValue.value) : 0;
    var annualIncome = parseFloat(salary) * 12 + parseFloat(bonus) - (parseFloat(socialHousingfund) + parseFloat(deductionValue) + parseFloat(base)) * 12;
    var taxListString = '';

    for (var i = 1; i <= 12; i++) {
        var currentMonthRemain = (salary - (socialHousingfund + deductionValue + base)) * i;
        currentMonthRemain = Math.max(currentMonthRemain, 0);
        if (currentMonthRemain > 0) {
            var taxPercentInfo = getPercent(currentMonthRemain);
            tax[i] = currentMonthRemain * taxPercentInfo[1] - taxPercentInfo[0] - sumArray(tax);
        } else {
            tax[i] = 0;
        }
        
        if (i === currentMonth) {
            var taxAmount = Math.max(tax[i], 0).toFixed(2);
            taxListString = taxAmount;
        }
    }

    document.getElementById("tax").innerHTML = taxListString;

    var socialTotal = (socialTax).toFixed(2);
    var housingfund = (housingfundTax).toFixed(2);
    var socialfundTotal = parseFloat(socialTotal) + parseFloat(housingfund)
    
    var personTotal = (parseFloat(socialTotal) + parseFloat(housingfund) + parseFloat(taxListString)).toFixed(2);
    $('#total').text(personTotal);

    var afterTaxIncome = (parseFloat(salary) - parseFloat(personTotal)).toFixed(2);
    $('#aftertax').text(afterTaxIncome);
    
    return { tax, socialfundTotal, annualIncome };
}

async function calcMonth(tax, socialfundTotal){

    var salary = parseInt(document.getElementById('salary').value);

    for (var i = 1; i <= 12; i++) {
        var monthlyIncome = parseFloat(salary) - parseFloat(socialfundTotal) - parseFloat(tax[i]);

    document.getElementById('monthincome' + i).textContent = monthlyIncome.toFixed(2);
    document.getElementById('monthtax' + i).textContent = tax[i].toFixed(2);

    }
}
                
async function calcAnnual(tax, annualIncome, customBaseHousing, customBaseSocial, housingPercentNormal) {
    let salary = parseFloat(document.getElementById('salary').value).toFixed(2);
    let bonusValue = document.getElementById('bonusinput');
    let bonus = bonusValue && bonusValue.value.trim() !== '' ? parseInt(bonusValue.value) : 0;

    let bonusTaxPercent = getPercentAnnual(bonus);
    let bonusTax = (bonus * bonusTaxPercent[1] - bonusTaxPercent[0]).toFixed(2);

    if (annualIncome > 0) {
        var annualTaxPercent = getPercent(annualIncome);
        var annualTax = (annualIncome * annualTaxPercent[1] - annualTaxPercent[0]).toFixed(2);
    } else {
        var annualTax = 0;
    }
    
    let totalTaxAll = tax.reduce((acc, curr) => acc + curr, 0);
    let totalTaxWithBonus = (parseFloat(bonusTax) + totalTaxAll).toFixed(2);
    // totalTaxWithBonus是综合收入的个税和年终奖的个税分开算
    // annualTax是年终奖合并到综合收入一起算的个税
    console.log(totalTaxWithBonus);
    console.log(annualTax);

    let annualTaxResult = (totalTaxWithBonus > annualTax) ? annualTax : totalTaxWithBonus;

    let housingfundToal = (customBaseHousing * housingPercentNormal * 12).toFixed(2);
    let socialTotal = ((customBaseSocial * (0.08 + 0.02 + 0.005)) * 12).toFixed(2);

    let annualNetSalary = (salary * 12 - annualTaxResult - parseFloat(socialTotal) - parseFloat(housingfundToal)).toFixed(2);
    let annualNetIncome = (parseFloat(annualNetSalary) + parseFloat(housingfundToal)).toFixed(2);
    const tableAnnual = document.querySelector('#detail');
    tableAnnual.innerHTML = '';

    tableAnnual.innerHTML = `
    <div id="detail" class="Flex item 1 w-75 me-5">
    <table class="table border border-2 border-light text-white text-center">
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
            <tr class="table-secondary">
            <th scope="row">税后年薪资</th>
            <td id="total">${annualNetSalary}</td>
            </tr>
            <tr class="table-dark">
            <th scope="row">税后年收入</th>
            <td id="aftertax">${annualNetIncome}</td>
            </tr>
        </tbody>
    </table>
    </div>
    `;

}

function resetToOriginalHtml() {
    const tableAnnual = document.querySelector('#detail');
    
    tableAnnual.innerHTML = '';
    tableAnnual.appendChild(originalHtml.cloneNode(true));
}


});

