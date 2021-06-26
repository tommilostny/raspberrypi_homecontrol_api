namespace RpiHomeHub.BlazorWeb.Models
{
    public class ColorModel
    {
        public string Name { get; set; }

        public ColorRGB Color { get; set; }
    }

    public class ColorRGB
    {
        public int Red { get; set; }
        public int Green { get; set; }
        public int Blue { get; set; }
    }

    public enum ColorMode
    {
        Yeelight, LED
    }
}
