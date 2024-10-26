
// Método para destacar a página selecionada
const currentPath = window.location.pathname;

const buttonId = currentPath.includes('Home')          ? 'homeBtn' :
                 currentPath.includes('CreateScreen')  ? 'createBtn' :
                 currentPath.includes('Imports')       ? 'importsBtn' :
                 currentPath.includes('Plots')         ? 'plotsBtn' :
                 currentPath.includes('Inputs')        ? 'inputsBtn' : null;

if( buttonId )
    document.getElementById(buttonId).classList.add('highlight');


// Métodos para criar sintaxe no html
function keywords(list, highlight, tag) {

    const elementos = document.querySelectorAll(tag); // Aplica ao corpo inteiro do documento

    elementos.forEach(elemento => {
        list.forEach(palavra => {

            const regex = new RegExp(`\\b(${palavra})\\b`, 'g'); // Regex para palavra exata
            elemento.innerHTML = elemento.innerHTML.replace(regex, `<span class="${highlight}">$1</span>`);
        });
    });
}

function keywordsRegex(highlightNumber, highlightString, highlightBrackets, tag) {

    const elementos = document.querySelectorAll(tag); // Aplica ao corpo inteiro do documento

    elementos.forEach(elemento => {
        // Captura o conteúdo atual
        let content = elemento.innerHTML;

        // Regex para strings entre aspas simples ou duplas
        const regexString = /(["'])(?:(?=(\\?))\2.)*?\1/g;
        
        // Armazena as strings temporariamente para não interferir na coloração dos números
        let stringMatches = [];
        content = content.replace(regexString, match => {
            stringMatches.push(match);
            return `__STRING_PLACEHOLDER__${stringMatches.length - 1}__`;
        });

        // Regex para números inteiros ou floats que NÃO estejam dentro de datas (YYYY-MM-DD HH:MM)
        const regexNumber = /\b\d+(\.\d+)?\b/g;

        // Substitui os números por <span> com a classe de coloração para números, exceto para números dentro de datas
        content = content.replace(regexNumber, match => {
            // Verifica se o número é parte de uma data ou estrutura semelhante
            if (/^\d{4}-\d{2}-\d{2}$/.test(match) || /^\d{2}:\d{2}$/.test(match)) {
                return match; // Não aplica coloração se for uma data ou hora
            }
            return `<span class="${highlightNumber}">${match}</span>`;
        });
        
        // Regex para capturar texto entre chaves {}, colchetes [], e parênteses ()
        const regexBrackets = /([{}\[\]()])/g;

        // Substitui o texto entre chaves, colchetes e parênteses por <span> com a classe de coloração para colchetes
        content = content.replace(regexBrackets, match => {
            return `<strong class="${highlightBrackets}">${match}</strong>`;
        });

        // Restaura as strings que foram substituídas pelos placeholders
        content = content.replace(/__STRING_PLACEHOLDER__(\d+)__/g, (placeholder, index) => {
            return `<span class="${highlightString}">${stringMatches[index]}</span>`;
        });

        // Atualiza o conteúdo HTML do elemento
        elemento.innerHTML = content;
    });
}

keywordsRegex('redColor', 'greenColor', 'bracketsColor', 'code')

const      keyword = ['def', 'if', 'else', 'for', 'while', 'in', 'import', 'from', 'as', 'try', 'except', 'pass'];
const        funcs = ['len', 'range', 'print', 'join', 'format_exception_only', 'strip', 'extract_tb', 'append'];
const      excepts = ['NameError', 'self', 'type'];
const        types = ['list', 'int', 'float', 'str', 'ctk', 'pd', 'bool'];
const       params = ['df', 'fig', 'symbol', 'number', 'value', 'pathFile', 'lstInputs', 'isHistogram', 'heightHistogram'];

const personalFunc = ['closes', 'highs', 'lows', 'opens', 'volumes', 'indexes', 'dates', 'size', 
                      'scientificNotation', 'formatNumber', 'decimalFormat',  
                      'shiftDateHours', 'shiftDateMinutes', 'selectDay', 'maxPrice', 'minPrice', 'indexMaxPrice', 'indexMinPrice', 'pdDatetime', 'indexByDate', 
                      'writeFile', 'readFile', 'writeInput', 'readingInput', 'console', 'MA', 'VWAP', 'STDDEV', 'ATR', 'mWriteLog', 'mConsole', 'hexcolorToRgba', 'valuesInList'];

const        plots = ['plotCandle', 'plotLines', 'plotLineColor', 'plotFill', 'plotHorizontalLine', 
                      'plotVerticalLine', 'plotHistogram', 'plotLabel', 'plotText', 'plotFigure'];

const       inputs = ['inputLabel', 'inputButton', 'inputCheckbox', 'inputCalendar', 'inputEntry', 'inputIntSpinbox', 'inputFloatSpinbox', 
                      'inputOptions', 'inputSlider', 'inputColor', 'inputDatetime', 'inputDatetime', 'createHSeparator', 'createVSeparator'];

keywords(keyword,      'parameterColor', 'code');
keywords(funcs,        'functionColor',  'code');
keywords(excepts,      'excepts',        'code');
keywords(personalFunc, 'personal',       'code');
keywords(params,       'params',         'code');
keywords(plots,        'plots',          'code');
keywords(inputs,       'plots',          'code');
keywords(types,        'types',          'code');

