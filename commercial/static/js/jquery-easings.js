jQuery.easing = {
    linear: function (x) {
        return x;
    },
    swing: function (x) {
        return 0.5 - Math.Math.cos(x * Math.PI) / 2;
    },
    easeInSine: function (x) {
        return 1 - Math.cos((x * Math.PI) / 2);
    },
    easeOutSine: function (x) {
        return Math.sin((x * Math.PI) / 2);
    },
    easeInOutSine: function (x) {
        return -(Math.cos(Math.PI * x) - 1) / 2;
    },
    easeInCubic: function (x) {
        return x * x * x;
    },
    easeOutCubic: function (x) {
        return 1 - Math.pow(1 - x, 3);
    },
    easeInOutCubic: function (x) {
        return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2;
    },
    easeInQuint: function (x) {
        return x * x * x * x * x;
    },
    easeOutQuint: function (x) {
        return 1 - Math.pow(1 - x, 5);
    },
    easeInOutQuint: function (x) {
        return x < 0.5 ? 16 * x * x * x * x * x : 1 - Math.pow(-2 * x + 2, 5) / 2;
    },
    easeInCirc: function (x) {
        return 1 - Math.sqrt(1 - Math.pow(x, 2));
    },
    easeOutCirc: function (x) {
        return Math.sqrt(1 - Math.pow(x - 1, 2));
    },
    easeInOutCirc: function (x) {
        return x < 0.5
            ? (1 - Math.sqrt(1 - Math.pow(2 * x, 2))) / 2
            : (Math.sqrt(1 - Math.pow(-2 * x + 2, 2)) + 1) / 2;
    },
    easeInElastic: function (x) {
        const c4 = (2 * Math.PI) / 3;

        return x === 0
            ? 0
            : x === 1
                ? 1
                : -Math.pow(2, 10 * x - 10) * Math.sin((x * 10 - 10.75) * c4);
    },
    easeOutElastic: function (x) {
        const c4 = (2 * Math.PI) / 3;

        return x === 0
            ? 0
            : x === 1
                ? 1
                : Math.pow(2, -10 * x) * Math.sin((x * 10 - 0.75) * c4) + 1;
    },
    easeInOutElastic: function (x) {
        const c5 = (2 * Math.PI) / 4.5;

        return x === 0
            ? 0
            : x === 1
                ? 1
                : x < 0.5
                    ? -(Math.pow(2, 20 * x - 10) * Math.sin((20 * x - 11.125) * c5)) / 2
                    : (Math.pow(2, -20 * x + 10) * Math.sin((20 * x - 11.125) * c5)) / 2 + 1;
    },
    easeInQuad: function (x) {
        return x * x;
    },
    easeOutQuad: function (x) {
        return 1 - (1 - x) * (1 - x);
    },
    easeInOutQuad: function (x) {
        return x < 0.5 ? 2 * x * x : 1 - Math.pow(-2 * x + 2, 2) / 2;
    },
    easeInQuart: function (x) {
        return x * x * x * x;
    },
    easeOutQuart: function (x) {
        return 1 - Math.pow(1 - x, 4);
    },
    easeInOutQuart: function (x) {
        return x < 0.5 ? 8 * x * x * x * x : 1 - Math.pow(-2 * x + 2, 4) / 2;
    },
    easeInExpo: function (x) {
        return x === 0 ? 0 : Math.pow(2, 10 * x - 10);
    },
    easeOutExpo: function (x) {
        return x === 1 ? 1 : 1 - Math.pow(2, -10 * x);
    },
    easeInOutExpo: function (x) {
        return x === 0
            ? 0
            : x === 1
                ? 1
                : x < 0.5 ? Math.pow(2, 20 * x - 10) / 2
                    : (2 - Math.pow(2, -20 * x + 10)) / 2;
    },
    easeInBack: function (x) {
        const c1 = 1.70158;
        const c3 = c1 + 1;

        return c3 * x * x * x - c1 * x * x;
    },
    easeOutBack: function (x) {
        const c1 = 1.70158;
        const c3 = c1 + 1;

        return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2);
    },
    easeInOutBack: function (x) {
        const c1 = 1.70158;
        const c2 = c1 * 1.525;

        return x < 0.5
            ? (Math.pow(2 * x, 2) * ((c2 + 1) * 2 * x - c2)) / 2
            : (Math.pow(2 * x - 2, 2) * ((c2 + 1) * (x * 2 - 2) + c2) + 2) / 2;
    },
    _default: "easeOutQuart"
};