// Rules and recipes are shared with Python; parity is enforced by tests/test_static.py.
const strip = s => s.replace(/^[\u0009-\u000d\u001c-\u0020\u0085\u00a0\u1680\u2000-\u200a\u2028\u2029\u202f\u205f\u3000]+|[\u0009-\u000d\u001c-\u0020\u0085\u00a0\u1680\u2000-\u200a\u2028\u2029\u202f\u205f\u3000]+$/gu, '');
const length = s => [...s].length;
export function renderRequest(data, styles, rules) {
  if (!data || typeof data !== 'object' || Array.isArray(data)) throw Error('请求必须是 JSON 对象');
  if (Object.keys(data).some(k => !['style_id','subject','purpose','aspect','caption','color_policy'].includes(k))) throw Error('存在未知输入字段');
  const style = styles.find(s => s.id === data.style_id || s.aliases?.includes(data.style_id));
  if (!style) throw Error('请选择有效风格');
  const {subject, purpose='single', aspect=null, caption=null, color_policy='ask'} = data;
  if (typeof subject !== 'string' || !strip(subject) || length(subject)>1200) throw Error('主题须为 1–1200 字符');
  if (!Object.hasOwn(rules.layouts,purpose) || !style.uses.includes(purpose)) throw Error('不支持的用途');
  if (!rules.aspects.includes(aspect)) throw Error('不支持的画幅比例');
  if (caption !== null && (typeof caption !== 'string' || length(caption)>80)) throw Error('标题最多 80 字符');
  if (!['ask','style','subject'].includes(color_policy)) throw Error('不支持的配色选择');
  const clean = strip(subject), title = caption ? strip(caption)||null : null;
  // Python's Unicode word boundaries differ from JavaScript's ASCII \b.
  const pattern = rules.colors.replaceAll('\\b','(?:(?<![\\p{L}\\p{N}_])(?=[\\p{L}\\p{N}_])|(?<=[\\p{L}\\p{N}_])(?![\\p{L}\\p{N}_]))');
  const hints = style.palette_limited ? [...new Set(clean.match(new RegExp(pattern,'giu'))||[])].sort() : [];
  const variant = Boolean(style.palette_limited && color_policy==='subject');
  const needsChoice = Boolean(hints.length && color_policy==='ask');
  const recipe = variant ? style.subject_palette_recipe : style.recipe;
  const parts = [recipe.split('{subject}').join(clean), rules.layouts[purpose]];
  if (style.palette_limited && color_policy==='style') parts.push(rules.style_choice);
  else if (variant) parts.push(rules.subject_choice);
  if (aspect) parts.push(rules.aspect_prefix+aspect);
  parts.push(title ? rules.caption : rules.no_caption);
  return {schema:rules.schema,style:{id:style.id,name:style.name,version:style.version,source:style.source},brief:{subject:clean,purpose,aspect,caption:title,color_policy},validation:style.validation,palette_variant:variant,color_hints:hints,warnings:[...(needsChoice?[rules.conflict]:[]),...(variant?[rules.variant]:[])],status:needsChoice?'needs_color_choice':'ready',prompt_zh:needsChoice?null:parts.join('\n\n')};
}
