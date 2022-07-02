export function getParameters(url) {
    const paramString = url.split('?')[1]
    const queryString = new URLSearchParams(paramString)
    let out = {}
    for (const pair of queryString.entries()) {
        out[pair[0]] = pair[1]
    }
    return out
}
