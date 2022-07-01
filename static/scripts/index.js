const advancedButton = document.querySelector("#advanced-button")
const priceMinSlider = document.querySelector("#price-min")
const priceMaxSlider = document.querySelector("#price-max")
let advancedOptionsShown = false

advancedButton.addEventListener("click", () => {
    const advancedOptions = document.querySelector("#advanced-search-options")
    advancedOptionsShown = !advancedOptionsShown
    if (advancedOptionsShown) {
        advancedOptions.style.display = "inline"
        advancedButton.innerHTML = "Show advanced"
        showPriceTooltip("#price-min-number", priceMinSlider)
        showPriceTooltip("#price-max-number", priceMaxSlider)
    } else {
        advancedOptions.style.display = "none"
        advancedButton.innerHTML = "Hide advanced"
    }
})

function showPriceTooltip(id, callerNode) {
    const priceValue = document.querySelector(id)
    const minVal = callerNode.min
    const maxVal = callerNode.max
    const value = callerNode.value
    const percent = (value - minVal) / (maxVal - minVal)
    const position = callerNode.offsetWidth * percent
    priceValue.style.left = `${position+100}px`
    priceValue.innerHTML = callerNode.value
}

priceMinSlider.addEventListener("input", () => showPriceTooltip("#price-min-number", priceMinSlider))
priceMaxSlider.addEventListener("input", () => showPriceTooltip("#price-max-number", priceMaxSlider))
