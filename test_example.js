// Test the specific example
const STOP_WORDS = new Set([
    'the','a','an','and','or','for','of','in','with','to','is','by','at','on',
    'all','new','free','per','mm','kg','ltr','litre','ml','pack','set','each',
    'pair','x','gst','excl','inc',
]);

function normalize(name) {
    name = name.toLowerCase().trim();
    name = name.replace(/[®™©�\u0000-\u001f]/g, '');
    name = name.replace(/\s*\(.*?\)\s*/g, ' ');
    for (const sep of [' - ', ' – ', ' — ']) {
        const i = name.indexOf(sep);
        if (i > 10) name = name.substring(0, i);
    }
    return name.replace(/\s+/g, ' ').trim();
}

function tokenize(name) {
    let norm = normalize(name);

    const brandNames = [
        'kevmor', 'intafloors', 'gibbon', 'trade', 'marques', 'gluesntools', 'homely',
        'mapei', 'ultrabond', 'nexus', 'rla', 'dnu', 'bostik', 'sika', 'ardex',
        'dunlop', 'selleys', 'roberts', 'henry', 'uzin', 'wakol', 'laticrete',
        'eco', 'premium', 'professional', 'pro', 'super', 'plus', 'max', 'ultra',
        'standard', 'general', 'purpose', 'gp', 'lv', 'xl', 'hd', 'heavy', 'duty'
    ];
    for (const brand of brandNames) {
        norm = norm.replace(new RegExp('\\b' + brand + '\\b', 'g'), '');
    }

    // Remove product codes
    norm = norm.replace(/\b\d{2,4}\b/g, '');

    const tokens = new Set(norm.match(/[a-z0-9]+/g) || []);
    STOP_WORDS.forEach(w => tokens.delete(w));
    return tokens;
}

function similarity(name1, name2) {
    const t1 = tokenize(name1);
    const t2 = tokenize(name2);
    if (!t1.size || !t2.size) return 0;
    let intersection = 0;
    t1.forEach(t => { if (t2.has(t)) intersection++; });
    const union = new Set([...t1, ...t2]).size;
    return intersection / union;
}

// Test with the user's example
const kevmor = 'Spartan Gripper Domestic Concrete Nail 5/8" (extra wide) - SFS7230W';
const gibbon = 'Spartan Gripper Domestic Concrete Nail 5/8-SFS 7230W';

console.log('Testing user example:\n');
console.log('Kevmor:', kevmor);
console.log('Gibbon:', gibbon);
console.log('\nAfter normalization:');
console.log('Kevmor:', normalize(kevmor));
console.log('Gibbon:', normalize(gibbon));
console.log('\nTokens:');
console.log('Kevmor:', [...tokenize(kevmor)].join(', '));
console.log('Gibbon:', [...tokenize(gibbon)].join(', '));
console.log('\nSimilarity:', (similarity(kevmor, gibbon) * 100).toFixed(1) + '%');
console.log('Match at 35%?', similarity(kevmor, gibbon) >= 0.35 ? 'YES ✓' : 'NO ✗');
