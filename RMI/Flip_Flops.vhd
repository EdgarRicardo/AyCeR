--Practica 2 - Flip-Flops --

library ieee;  --paqueteria ieee
use ieee.std_logic_1164.all; --1164

entity FlipFlop is port (  --definicion de la entidad
	S,R,D,J,K,T: in std_logic; --Flip Flops entradas
	CLK: in std_logic; --Señal de reloj
	PRE,CLR: in std_logic;
	Q,NQ: inout std_logic;
	sel: in std_logic_vector(1 downto 0)
);
end FlipFlop;

architecture A_FlipFlop of FlipFlop is  --desarrollo de la arquitectura
begin	


	PROCESS(S,R,CLK,PRE,CLR)
	BEGIN
		if(CLR='0')then
			Q<='0';
			NQ<='1';
		elsif(CLK'EVENT AND CLK='1') then --espera hasta que ocurra
			if(PRE='1')then
				Q<='1';
				NQ<='0';
			elsif(sel="00")then
				Q<= D;
				NQ<= not D;
			elsif (sel="01")then
				Q<= S or ((not R)and Q);
				NQ<= not (S or ((not R)and Q));
			elsif(sel="10")then
				Q<= ((not K) and Q) or (J and (not Q));
				NQ<= not (((not K) and Q) or (J and (not Q)));
			elsif(sel="11")then
				Q<= ((not T)and Q) or (T and (not Q));
				NQ<= not(((not T)and Q) or (T and (not Q)));
			end if;
		end if;

	END PROCESS;

end architecture;