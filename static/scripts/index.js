import { getParameters } from "./url.js"
const advancedButton = document.querySelector("#advanced-button")
const userPrompt = document.querySelector("#user-prompt")
const searchCount = document.querySelector("#search-count")
const priceMinSlider = document.querySelector("#price-min")
const priceMaxSlider = document.querySelector("#price-max")
let advancedOptionsShown = false

advancedButton.addEventListener("click", () => {
    const advancedOptions = document.querySelector("#advanced-search-options")
    advancedOptionsShown = !advancedOptionsShown
    if (advancedOptionsShown) {
        advancedOptions.style.display = "inline"
        advancedButton.innerHTML = "Hide advanced"
        showPriceTooltip("#price-min-number", priceMinSlider)
        showPriceTooltip("#price-max-number", priceMaxSlider)
    } else {
        advancedOptions.style.display = "none"
        advancedButton.innerHTML = "Show advanced"
    }
})

function setFormFieldsFromUrl() {
    const values = getParameters(window.location.href)
    if (values["q"]) { userPrompt.value = values["q"] }
    if (values["search-count"]) { searchCount.value = values["search-count"] }
    if (values["price-min"]) { priceMinSlider.value = values["price-min"] }
    if (values["price-max"]) { priceMaxSlider.value = values["price-max"] }
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
setFormFieldsFromUrl()
priceMinSlider.addEventListener("input", () => showPriceTooltip("#price-min-number", priceMinSlider))
priceMaxSlider.addEventListener("input", () => showPriceTooltip("#price-max-number", priceMaxSlider))
