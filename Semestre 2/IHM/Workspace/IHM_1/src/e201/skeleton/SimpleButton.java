
package e201.skeleton ;
import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Font;
import java.awt.Paint;
import java.awt.Stroke;

import javax.swing.JFrame;

import fr.lri.swingstates.canvas.CRectangle;
import fr.lri.swingstates.canvas.CShape;
import fr.lri.swingstates.canvas.CStateMachine;
import fr.lri.swingstates.canvas.CText;
import fr.lri.swingstates.canvas.Canvas;
import fr.lri.swingstates.canvas.transitions.ClickOnShape;
import fr.lri.swingstates.canvas.transitions.EnterOnShape;
import fr.lri.swingstates.canvas.transitions.LeaveOnShape;
import fr.lri.swingstates.canvas.transitions.ReleaseOnShape;
import fr.lri.swingstates.debug.StateMachineVisualization;
import fr.lri.swingstates.sm.State;
import fr.lri.swingstates.sm.Transition;

/**
 * @author Nicolas Roussel (roussel@lri.fr)
 *
 */
public class SimpleButton {

    private CText label ;
    private CRectangle rect;

    SimpleButton(Canvas canvas, String text) {
	   label = canvas.newText(5, 5, text, new Font("verdana", Font.PLAIN, 12));
	   rect = canvas.newRectangle(0, 0, label.getWidth()+10, label.getHeight()+10);
	   label.above(rect);
	   label.setPickable(false);
	   rect.addChild(label);
	   
	   CStateMachine sm = new CStateMachine() {
		    Stroke initStroke;
		    Paint initColor;
		    public State idle = new State() {
		        Transition idleToHover = new EnterOnShape(">> hover") {
		            public void action() {
		                initStroke = getShape().getStroke();
		                initColor = getShape().getFillPaint();
		                getShape().setStroke(new BasicStroke(2));
		            }
		        };
		    };
		    public State hover = new State() {
		    	 Transition hoverToIdle = new LeaveOnShape(">> idle") {
			            public void action() {
			            	getShape().setStroke(initStroke);
			            }
			        };
			        Transition hoverToClick = new ClickOnShape(">> clicked") {
			            public void action() {
			            	System.out.println("Click");
			            	getShape().setStroke(initStroke);
			            	getShape().setFillPaint(Color.YELLOW);
			            }
			        };
		    };
		    
		    public State clicked = new State() {
			        Transition clickToHover= new ReleaseOnShape(">> hover") {
			            public void action() {
			            	System.out.println("release");
			            	getShape().setStroke(new BasicStroke(2));
			            	getShape().setFillPaint(initColor);
			            }
			        };
			        
		    };
		};
		
		JFrame viz = new JFrame() ;
		viz.getContentPane().add(new StateMachineVisualization(sm));
		viz.pack() ;
		viz.setVisible(true) ;
		
		sm.attachTo(canvas);
	
	   
    }

    public void action() {
	   System.out.println("ACTION!") ;
    }

    public CShape getShape() {
	   return rect ;
    }

    static public void main(String[] args) {
	   JFrame frame = new JFrame() ;
	   Canvas canvas = new Canvas(400,400) ;
	   frame.getContentPane().add(canvas) ;
	   frame.pack() ;
	   frame.setVisible(true) ;

	   SimpleButton simple = new SimpleButton(canvas, "simple") ;
	   simple.getShape().translateBy(100,100) ;
    }

}
