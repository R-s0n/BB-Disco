const puppeteer = require('puppeteer');

function getHtml(){
    const url = "https://hackerone.com/directory/programs?order_direction=DESC&order_field=started_accepting_at"
    try {
        (async () => {
            const browser = await puppeteer.launch();
            const page = await browser.newPage();
            try {
                await page.goto(url, {
                    waitUntil: 'networkidle0'
                });
            } catch (error) {
                console.log(error);
                process.exit(1);
            }
            try {
                const data = await page.content();
                console.log(data);
            } catch (error) {
                console.log(error);
                process.exit(1);
            }

            try {
                await browser.close();
            } catch (error) {
                console.log(error);
                process.exit(1);
            }
        })();
    } catch (error) {
        console.log(error);
        process.exit(1);
    }
}

getHtml();