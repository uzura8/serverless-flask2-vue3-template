type TransformableItem = { [key: string]: any }

export function transformKey(
  items: TransformableItem[],
  oldKey: string,
  newKey: string
): TransformableItem[] {
  return items.map((item) => {
    if (!(oldKey in item)) return item

    const { [oldKey]: oldValue, ...rest } = item
    return { ...rest, [newKey]: oldValue }
  })
}
