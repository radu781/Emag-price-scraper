import { getParameters } from "./url.js"

const advancedButton = document.querySelector("#advanced-button")
const userPrompt = document.querySelector("#user-prompt")
const searchCount = document.querySelector("#search-count")
const priceMinSlider = document.querySelector("#price-min")
const priceMaxSlider = document.querySelector("#price-max")
setFormFieldsFromUrl()

let advancedOptionsShown = searchCount.value !== "" || priceMinSlider.value != 0 || priceMaxSlider.value != 0
console.log(searchCount.value, priceMinSlider.value, priceMaxSlider.value, advancedOptionsShown)
toggleAdvancedSearch()

advancedButton.addEventListener("click", () => {
    toggleAdvancedSearch()
})

function toggleAdvancedSearch() {
    const advancedOptions = document.querySelector("#advanced-search-options")
    if (advancedOptionsShown) {
        advancedOptions.style.display = "flex"
        advancedButton.innerHTML = "Hide advanced"
        showPriceTooltip("#price-min-number", priceMinSlider)
        showPriceTooltip("#price-max-number", priceMaxSlider)
    } else {
        advancedOptions.style.display = "none"
        advancedButton.innerHTML = "Show advanced"
    }
    advancedOptionsShown = !advancedOptionsShown
}

function setFormFieldsFromUrl() {
    const values = getParameters(window.location.href)
    if (values["q"]) { userPrompt.value = values["q"] }
    if (values["search-count"]) { searchCount.value = values["search-count"] }
    if (values["price-min"]) {
        priceMinSlider.value = values["price-min"]
    } else {
        priceMinSlider.value = 0
    }
    if (values["price-max"]) {
        priceMaxSlider.value = values["price-max"]
    } else {
        priceMaxSlider.value = 0
    }
}

function showPriceTooltip(id, callerNode) {
    const priceValue = document.querySelector(id)
    const minVal = callerNode.min
    const maxVal = callerNode.max
    const value = callerNode.value
    const percent = (value - minVal) / (maxVal - minVal)
    const position = callerNode.offsetWidth * percent
    priceValue.style.left = `${position + 100}px`
    priceValue.innerHTML = callerNode.value
}
priceMinSlider.addEventListener("input", () => showPriceTooltip("#price-min-number", priceMinSlider))
priceMaxSlider.addEventListener("input", () => showPriceTooltip("#price-max-number", priceMaxSlider))